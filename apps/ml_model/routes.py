from flask import Blueprint, request, jsonify
from .util import test_model_and_preprocessing
from apps.ml_model import blueprint  


@blueprint.route('/predict', methods=['POST'])
def predict():
    try:
       
        model_path = "apps/ml_model/model_v9.pth"
        image_file = request.files['image']

      
        image_path = "temp_image.jpg"
        image_file.save(image_path)

        # Call the test function
        result = test_model_and_preprocessing(model_path, image_path)

        # Return the result
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
