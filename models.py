from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dispositivo = db.Column(db.String(64), nullable=False)
    disciplina = db.Column(db.String(64), nullable=False)
    