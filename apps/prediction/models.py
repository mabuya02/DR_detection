from datetime import datetime,timezone
from apps import db
from flask_sqlalchemy import SQLAlchemy

class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id', ondelete='CASCADE'), nullable=False)
    model_version = db.Column(db.String(50), nullable=False)
    predicted_label = db.Column(db.Integer, nullable=False)
    confidence_score = db.Column(db.Numeric(7, 4), nullable=True)
    grad_cam_path = db.Column(db.String(255), nullable=True)  
    predicted_at = db.Column(db.DateTime,  default=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime,  default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    patient = db.relationship('Patient', backref='predictions', lazy=True)
    image = db.relationship('Image', backref='predictions', lazy=True)

    def __init__(self, patient_id, image_id, model_version, predicted_label, confidence_score=None, grad_cam_path=None):
        """
        Initialize the Prediction instance.
        """
        self.patient_id = patient_id
        self.image_id = image_id
        self.model_version = model_version
        self.predicted_label = predicted_label
        self.confidence_score = confidence_score
        self.grad_cam_path = grad_cam_path  

    def __repr__(self):
        """
        Represent the Prediction instance as a string.
        """
        return (f"<Prediction ID {self.id}, Patient ID {self.patient_id}, Image ID {self.image_id}, "
                f"Model {self.model_version}, Predicted Label {self.predicted_label}, "
                f"Confidence {self.confidence_score}, Grad-CAM Path {self.grad_cam_path}>")
