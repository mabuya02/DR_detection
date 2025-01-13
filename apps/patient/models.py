from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy
from apps.image.models import Image 
from apps import db


  
class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    blood_type = db.Column(db.String(10))
    status = db.Column(db.String(20), default='active') 


    def __init__(self, first_name, last_name, dob, gender=None, phone_number=None, email=None, 
                 medical_history=None, allergies=None, emergency_contact_name=None, 
                 emergency_contact_phone=None, address=None, blood_type=None,status = 'active'):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.phone_number = phone_number
        self.email = email
        self.medical_history = medical_history
        self.allergies = allergies
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.address = address
        self.status = status
        self.blood_type = blood_type
     

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"


