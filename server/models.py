from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from config import db

db = SQLAlchemy()

# Models go here!

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    patients = relationship('PatientDoctor', back_populates='doctor') 

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    appointments = relationship('Appointment', back_populates='patient')  
    doctors = relationship('PatientDoctor', back_populates='patient')  

class PatientDoctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    relationship_type = db.Column(db.String(100), nullable=False)  
    
    user = relationship('Doctor', back_populates='patients')
    patient = relationship('Patient', back_populates='doctor')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='Scheduled', nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    
    patient = relationship('Patient', back_populates='appointments')
    sessions = relationship('Session', back_populates='appointment', cascade='all, delete-orphan')


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=True)
    treatment_plan = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    appointment = relationship('Appointment', back_populates='sessions')

