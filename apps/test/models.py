from apps import db
from datetime import datetime

class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    test_type = db.Column(db.String(100), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    result = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    conducted_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    left_eye_id = db.Column(db.Integer, db.ForeignKey('predictions.id', ondelete='SET NULL'), nullable=True)
    right_eye_id = db.Column(db.Integer, db.ForeignKey('predictions.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', backref='tests', lazy=True)
    conducted_by_user = db.relationship('Users', backref='conducted_tests', lazy=True)
    left_eye_prediction = db.relationship('Prediction', foreign_keys=[left_eye_id], backref='left_eye_test', lazy=True)
    right_eye_prediction = db.relationship('Prediction', foreign_keys=[right_eye_id], backref='right_eye_test', lazy=True)

    def __repr__(self):
        return (f"<Test {self.test_type} for Patient {self.patient_id}, "
                f"Left Eye Prediction {self.left_eye_id}, Right Eye Prediction {self.right_eye_id}>")
