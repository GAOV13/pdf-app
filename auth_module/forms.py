from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    """
    Formulario de registro de usuario.

    Campos:
    - email (StringField): Correo electrónico del usuario.
    - password (PasswordField): Contraseña del usuario.
    - confirm_password (PasswordField): Confirmación de la contraseña.
    - submit (SubmitField): Botón para enviar el formulario.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    Formulario de inicio de sesión de usuario.

    Campos:
    - email (StringField): Correo electrónico del usuario.
    - password (PasswordField): Contraseña del usuario.
    - submit (SubmitField): Botón para enviar el formulario.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TwoFactorForm(FlaskForm):
    """
    Formulario de verificación de doble factor.

    Campos:
    - otp (StringField): Código OTP generado por la aplicación de autenticación.
    - submit (SubmitField): Botón para enviar el formulario.
    """
    otp = StringField('OTP', validators=[DataRequired()])
    submit = SubmitField('Verify')