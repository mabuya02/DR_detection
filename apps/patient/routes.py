from flask import render_template, request, redirect, url_for,flash
from apps.patient import blueprint  
from apps.patient.models import Patient 
from apps.image.models import Image
from apps.test.models import Test 
from apps.prediction.models import Prediction
from apps import db
from datetime import datetime




@blueprint.route('/list')
def patient_list():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    today = datetime.today()
    for patient in patients:
        birth_date = patient.dob
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        patient.age = age
    
    return render_template('patients/patient_list.html', patients=patients)


@blueprint.route('/view/<int:patient_id>', methods=['GET'])
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    today = datetime.today()
    birth_date = patient.dob
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    patient.age = age 
    return render_template('patients/view_patient.html', patient=patient)

@blueprint.route('/patients/<int:patient_id>/edit', methods=['GET'])
def edit_patient_form(patient_id):
    patient = Patient.query.get_or_404(patient_id) 
    return render_template('patients/edit_patient.html', patient=patient)

@blueprint.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id) 

    if request.method == 'POST':
        # Get updated data from the form
        patient.first_name = request.form['first_name']
        patient.last_name = request.form['last_name']
        patient.dob = request.form['dob']
        patient.gender = request.form['gender']
        patient.phone_number = request.form['phone_number']
        patient.email = request.form['email']
        patient.medical_history = request.form['medical_history']
        patient.allergies = request.form['allergies']
        patient.emergency_contact_name = request.form['emergency_contact_name']
        patient.emergency_contact_phone = request.form['emergency_contact_phone']
        patient.address = request.form['address']
        patient.blood_type = request.form['blood_type']

        # Validate the form fields
        errors = []
        if not patient.first_name or not patient.last_name or not patient.dob:
            errors.append('First name, last name, and date of birth are required.')
        if not patient.email:
            errors.append('Email is required.')

        if errors:
            return render_template('edit_patient.html', patient=patient, messages={'category': 'danger', 'messages': errors})

        # Save changes to the database
        db.session.commit()

        # Flash success message
        flash('Patient updated successfully!', 'success')

        # Redirect to the patient list or detail view
        return redirect(url_for('patient_blueprint.patient_list'))

    # Render the edit form with existing patient data
    return render_template('patients/edit_patient.html', patient=patient)


@blueprint.route('/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    try:
        predictions = Prediction.query.filter_by(patient_id=patient.id).all()
        for prediction in predictions:
            prediction.patient_id = '#'
        
        tests = Test.query.filter_by(patient_id=patient.id).all()
        for test in tests:
            test.patient_id = '#'

        images = Image.query.filter_by(patient_id=patient.id).all()
        for image in images:
            image.patient_id = '#'

        db.session.commit()

        db.session.delete(patient)
        db.session.commit()

        flash('Patient and related records updated successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error updating patient and related records: {str(e)}', 'danger')

    return redirect(url_for('patient_blueprint.patient_list'))
 




@blueprint.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        email = request.form['email']
        medical_history = request.form['medical_history']
        allergies = request.form['allergies']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_phone = request.form['emergency_contact_phone']
        address = request.form['address']
        blood_type = request.form['blood_type']

        errors = []

        # Validate required fields
        if not first_name or not last_name or not dob:
            errors.append('First name, last name, and date of birth are required.')
        if not email:
            errors.append('Email is required.')

        if errors:
            return render_template('patients/add_patient.html', messages={'category': 'danger', 'messages': errors})

        # Convert the dob from string to datetime.date object
        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()  # Ensure correct date format (YYYY-MM-DD)
        except ValueError:
            errors.append('Invalid date format for Date of Birth.')
            return render_template('patients/add_patient.html', messages={'category': 'danger', 'messages': errors})

        # Create a new Patient instance
        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            dob=dob,  # Store as datetime.date
            gender=gender,
            phone_number=phone_number,
            email=email,
            medical_history=medical_history,
            allergies=allergies,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            address=address,
            blood_type=blood_type
        )

        # Save the patient to the database
        db.session.add(new_patient)
        db.session.commit()

        # Flash success message
        flash('Patient added successfully!', 'success')

        # Redirect to the patient list page or show a success message
        return redirect(url_for('patient_blueprint.patient_list'))

    return render_template('patients/add_patient.html')