import torch
from torchvision import transforms
from PIL import Image
from .load_model import load_model
from .grad_cam import GradCam

# Preprocessing for image (same as during training)
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

# Prediction function (including confidence score)
def predict(model, image_tensor):
    with torch.no_grad():
        output = model(image_tensor)
        probs = torch.nn.functional.softmax(output, dim=1)
        confidence, predicted = torch.max(probs, 1)
        return predicted.item(), confidence.item(), probs[0].tolist()

# Combined function for model loading, preprocessing, and prediction
def test_model_and_preprocessing(model_path, image_path):
    try:
        # Test loading the model
        model = load_model(model_path)
        print(f"Model loaded successfully from {model_path}")

        # Test image preprocessing
        image_tensor = preprocess_image(image_path)
        print(f"Image preprocessed successfully. Shape: {image_tensor.shape}")

        # Make prediction
        prediction, confidence, probs = predict(model, image_tensor)
        print(f"Prediction: Class {prediction}, Confidence: {confidence*100:.2f}%")
        print(f"Class probabilities: {probs}")

    except Exception as e:
        print(f"Error during model loading, image preprocessing, or prediction: {e}")

def model_prediction(model, image_tensor):
    # Make the model prediction
    output = model(image_tensor)
    predicted_class = output.argmax(dim=1).item()
    confidence = torch.softmax(output, dim=1)[0][predicted_class].item() * 100 
    return predicted_class, confidence



def generate_grad_cam(model, image_tensor, target_layer):
    grad_cam = GradCam(model, target_layer)
    grad_cam_image = grad_cam.generate_grad_cam(image_tensor)

    return grad_cam_image