import os
import cv2
import torch

from flask import render_template, request, redirect, url_for, flash,send_from_directory
from werkzeug.utils import secure_filename
from apps.ml_model.grad_cam import GradCam
from apps.test import blueprint
from apps.test.models import Test
from apps.image.models import Image
from apps.patient.models import Patient
from apps.prediction.models import Prediction
from apps import db
from datetime import datetime
from apps.ml_model.util import load_model, preprocess_image, model_prediction
from flask_login import current_user, login_required


MODEL_PATH = os.getenv('MODEL_PATH', 'apps/ml_model/model_v9.pth')
MEDIA_FOLDER = os.getenv('MEDIA_FOLDER', 'apps/static/assets/images/media/retinal_images')
GRAD_CAM_FOLDER = os.getenv('GRAD_CAM_FOLDER', 'apps/static/assets/images/media/grad_cam')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


PREDICTION_LABELS = {
    0: "No Diabetic Retinopathy",
    1: "Early Stage Diabetic Retinopathy",
    2: "Moderate Stage Diabetic Retinopathy",
    3: "Severe Diabetic Retinopathy",
    4: "Proliferative Diabetic Retinopathy"
}


def allowed_file(filename):
    """Check if a file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, folder):
    """Save an uploaded file and return its path."""
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    save_path = os.path.normpath(os.path.join(folder, filename))  
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
    file.save(save_path)
    
    return save_path


def save_grad_cam_image(image, filename):
    """Save the Grad-CAM image and return its path."""
    os.makedirs(GRAD_CAM_FOLDER, exist_ok=True)
    save_path = os.path.normpath(os.path.join(GRAD_CAM_FOLDER, filename))  
    cv2.imwrite(save_path, image)
    
    return save_path



@blueprint.route('/test_list')
@login_required
def test_list():
    tests = Test.query.all()
    tests = tests[::-1] 
    return render_template('tests/test_list.html', tests=tests)


@blueprint.route('/view/test/<int:test_id>', methods=['GET'])
@login_required
def view_test(test_id):
    test = Test.query.get(test_id)

    if test is None:
        flash('Test not found', 'danger')
        return redirect(url_for('test_blueprint.test_list'))

    left_eye_prediction = Prediction.query.get(test.left_eye_id)
    right_eye_prediction = Prediction.query.get(test.right_eye_id)

    # Retrieve the associated images
    left_eye_image = left_eye_prediction.image if left_eye_prediction else None
    right_eye_image = right_eye_prediction.image if right_eye_prediction else None

    # Map the prediction labels to their corresponding names
    left_eye_prediction_label = PREDICTION_LABELS.get(left_eye_prediction.predicted_label) if left_eye_prediction else None
    right_eye_prediction_label = PREDICTION_LABELS.get(right_eye_prediction.predicted_label) if right_eye_prediction else None

    test_results = {
        "test_id": test.id,
        "test_type": test.test_type,
        "test_date": test.test_date,
        "result": test.result,
        "status": test.status,
        "left_eye_prediction": left_eye_prediction,
        "right_eye_prediction": right_eye_prediction,
        "left_eye_prediction_label": left_eye_prediction_label,
        "right_eye_prediction_label": right_eye_prediction_label,
        "test_patient_firstname": test.patient.first_name,
        "test_patient_lastname": test.patient.last_name,
        "patient_gender": test.patient.gender,
        "patient_email": test.patient.email,
        "patient_phone_number": test.patient.phone_number,
        "left_eye_grad_cam_path": left_eye_prediction.grad_cam_path if left_eye_prediction else None,
        "right_eye_grad_cam_path": right_eye_prediction.grad_cam_path if right_eye_prediction else None,
        "left_eye_image_filename": left_eye_image.image_filename if left_eye_image else None,
        "right_eye_image_filename": right_eye_image.image_filename if right_eye_image else None,
    }

    return render_template('tests/view_test.html', test_results=test_results)


@blueprint.route('/fetch-grad-cam-image/<filename>')
def fetch_grad_cam_image(filename):
    # Safely serve the requested image from the grad_cam folder
    return send_from_directory( filename)

@blueprint.route('/create_test/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def create_test(patient_id):
    patient = Patient.query.get(patient_id)

    if patient is None:
        flash('Patient not found', 'danger')
        return redirect(url_for('test_blueprint.test_list'))

    today = datetime.today()
    birth_date = patient.dob
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if request.method == 'POST':
        # File uploads
        left_eye_image = request.files.get('left_eye_image')
        right_eye_image = request.files.get('right_eye_image')

        # Load model
        model = load_model(MODEL_PATH)
        grad_cam_generator = GradCam(model, model.features[-1][-1])  

        predictions = {
            "left_eye": {"file": left_eye_image, "grad_cam_path": None, "prediction": None},
            "right_eye": {"file": right_eye_image, "grad_cam_path": None, "prediction": None},
        }

        for eye, data in predictions.items():
            if data["file"] and allowed_file(data["file"].filename):
                # Save image
                file_path = save_file(data["file"], MEDIA_FOLDER)

                # Save image to database
                db_image = Image(patient_id=patient.id, image_filename=file_path)
                db.session.add(db_image)
                db.session.commit()

                # Preprocess and predict
                image_tensor = preprocess_image(file_path)
                pred_label, confidence = model_prediction(model, image_tensor)

                # Generate Grad-CAM
                heatmap = grad_cam_generator.generate_cam(image_tensor)
                grad_cam_image = grad_cam_generator.overlay_heatmap(heatmap, image_tensor)
                grad_cam_filename = f"{os.path.basename(file_path).rsplit('.', 1)[0]}_grad_cam.jpg"
                grad_cam_path = save_grad_cam_image(grad_cam_image, grad_cam_filename)

                # Save prediction to database
                prediction_record = Prediction(
                    patient_id=patient.id,
                    image_id=db_image.id,
                    model_version="v9",
                    predicted_label=pred_label,
                    confidence_score=confidence,
                    grad_cam_path=grad_cam_path,
                )
                db.session.add(prediction_record)
                db.session.commit()

                data["grad_cam_path"] = grad_cam_path
                data["prediction"] = prediction_record

        # Create and save test
        test_result = f"Left Eye: {PREDICTION_LABELS.get(predictions['left_eye']['prediction'].predicted_label, 'Unknown')}, Right Eye: {PREDICTION_LABELS.get(predictions['right_eye']['prediction'].predicted_label, 'Unknown')}"
        test = Test(
            patient_id=patient.id,
            test_type="retinal scanning",
            test_date=datetime.today().date(),
            result=test_result,
            status="Complete",
            conducted_by=current_user.id,
            left_eye_id=predictions['left_eye']['prediction'].id,
            right_eye_id=predictions['right_eye']['prediction'].id,
        )
        db.session.add(test)
        db.session.commit()

        flash('Test created and predictions saved successfully!', 'success')
        return redirect(url_for('test_blueprint.test_list'))

    return render_template('tests/create_test.html', patient=patient, age=age)
