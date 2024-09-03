from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from datetime import datetime
from auth_module.models import db, User  # Importa db y User aquí

class Document(db.Model):
    """
    Modelo de documento para la gestión de archivos subidos.

    Atributos:
    - id (int): ID del documento.
    - title (str): Título del documento.
    - description (str): Descripción del documento.
    - file_path (str): Ruta del archivo del documento.
    - uploaded_by (int): ID del usuario que subió el documento.
    - approved_by (int): ID del usuario que aprobó el documento.
    - timestamp (datetime): Fecha y hora de subida del documento.
    - approved (bool): Indica si el documento ha sido aprobado.

    Relaciones:
    - uploader (User): Usuario que subió el documento.
    - approver (User): Usuario que aprobó el documento.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)

    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref='uploaded_documents')
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_documents')