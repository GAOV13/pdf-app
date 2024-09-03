from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import pyotp

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    two_factor_secret = db.Column(db.String(16), nullable=True)
    is_approved = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_otp_uri(self):
        return pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(self.email, issuer_name="YourAppName")

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token)
