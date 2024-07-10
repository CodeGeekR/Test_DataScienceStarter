from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # Add this line to import the datetime module
# from flask_sqlalchemy import SQLAlchemy
from app import db

# db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    activo = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_profile(self, first_name=None, last_name=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        db.session.commit()

# Tabla Resultado del form ciencia de datos
class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dispositivo = db.Column(db.String(36), nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)
    puntaje_estadistica = db.Column(db.Integer, nullable=False)
    puntaje_aprendizaje_automatico = db.Column(db.Integer, nullable=False)
    puntaje_analisis_de_datos = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)