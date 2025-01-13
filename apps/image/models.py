from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from apps import db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    image_data = db.Column(db.LargeBinary)
    image_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) 

    def __init__(self, patient_id, image_filename, image_data=None, image_type=None):
        self.patient_id = patient_id
        self.image_filename = image_filename
        self.image_data = image_data
        self.image_type = image_type

    def __repr__(self):
        return f"<Image {self.image_filename}>"
