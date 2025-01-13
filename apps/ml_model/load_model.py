import torch
from torchvision import models
import torch.nn as nn
from torchvision.models import EfficientNet_B0_Weights

def load_model(model_path):
    # Load the model with weights as the latest preferred approach
    model = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT) 

    # Modify the classifier to match your specific task
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, 128),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(128, 5) 
    )

    # Load the custom model weights
    model.load_state_dict(torch.load(model_path, weights_only=True))  
    model.eval() 
    return model
