import torch
import numpy as np
import cv2
from torch.nn.functional import interpolate


class GradCam:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Register hooks
        self.target_layer.register_forward_hook(self.save_activations)
        self.target_layer.register_backward_hook(self.save_gradients)

    def save_activations(self, module, input, output):
        self.activations = output

    def save_gradients(self, module, grad_in, grad_out):
        self.gradients = grad_out[0]

    def forward(self, input_image):
        return self.model(input_image)

    def backward(self, class_idx):
        self.model.zero_grad()
        class_idx.backward()

    def generate_cam(self, input_image, target_class_idx=None):
        # Forward pass
        output = self.forward(input_image)

        # Target class: use max score if not provided
        if target_class_idx is None:
            target_class_idx = torch.argmax(output, dim=1)
        target = output[:, target_class_idx]
        
        # Backward pass
        self.backward(target)

        # Process gradients and activations
        gradients = self.gradients
        activations = self.activations
        weights = torch.mean(gradients, dim=(2, 3), keepdim=True) 
        cam = torch.sum(weights * activations, dim=1).squeeze(0)

        # ReLU and normalize
        cam = torch.clamp(cam, min=0)
        cam -= cam.min()
        cam /= cam.max()

        # Resize to input image size
        cam = interpolate(cam.unsqueeze(0).unsqueeze(0), size=(input_image.shape[2], input_image.shape[3]), mode="bilinear").squeeze()
        return cam.cpu().detach().numpy()

    def overlay_heatmap(self, heatmap, original_image):
        # Normalize the original image for display
        original_image = original_image.squeeze(0).cpu().numpy().transpose(1, 2, 0)
        original_image = np.uint8(255 * (original_image - original_image.min()) / (original_image.max() - original_image.min()))

        # Convert heatmap to RGB
        heatmap = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
        heatmap = np.float32(heatmap) / 255

        # Superimpose heatmap on the original image
        cam = 0.5 * heatmap + 0.5 * np.float32(original_image) / 255
        cam = cam / np.max(cam)
        return np.uint8(255 * cam)

    def save_grad_cam(self, cam_image, save_path):
        cv2.imwrite(save_path, cam_image)



