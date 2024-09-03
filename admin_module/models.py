from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from auth_module.models import db, User

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    user = db.relationship('User', backref=db.backref('admin_profile', uselist=False))