from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Modelo de usuario para la autenticación y autorización.

    Atributos:
    - id (int): ID del usuario.
    - email (str): Correo electrónico del usuario.
    - password_hash (str): Hash de la contraseña del usuario.
    - otp_secret (str): Secreto para la autenticación de dos factores.
    - is_authenticated_2fa (bool): Indica si el usuario ha autenticado con 2FA.

    Métodos:
    - set_password(password): Establece el hash de la contraseña.
    - check_password(password): Verifica la contraseña.
    - get_totp_uri(): Obtiene la URI para la configuración de TOTP.
    - verify_totp(token): Verifica el token TOTP.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False, default=pyotp.random_base32)
    is_authenticated_2fa = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """
        Establece el hash de la contraseña del usuario.

        Entradas:
        - password (str): Contraseña en texto plano.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica la contraseña del usuario.

        Entradas:
        - password (str): Contraseña en texto plano.

        Salidas:
        - bool: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password_hash(self.password_hash, password)

    def get_totp_uri(self):
        """
        Obtiene la URI para la configuración de TOTP.

        Salidas:
        - str: URI para la configuración de TOTP.
        """
        return f'otpauth://totp/YourApp:{self.email}?secret={self.otp_secret}&issuer=YourApp'

    def verify_totp(self, token):
        """
        Verifica el token TOTP.

        Entradas:
        - token (str): Token TOTP.

        Salidas:
        - bool: True si el token es válido, False en caso contrario.
        """
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)