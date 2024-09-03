from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False, default=pyotp.random_base32)
    is_authenticated_2fa = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        return f'otpauth://totp/YourApp:{self.email}?secret={self.otp_secret}&issuer=YourApp'

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)