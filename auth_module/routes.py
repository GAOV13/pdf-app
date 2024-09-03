import qrcode
from io import BytesIO
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, db
from .forms import RegistrationForm, LoginForm, TwoFactorForm

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Maneja el registro de nuevos usuarios.

    Entradas:
    - Ninguna (obtiene datos del formulario de registro).

    Salidas:
    - Renderiza la plantilla de registro con el formulario y, si es exitoso, muestra un mensaje de éxito y el código QR para 2FA.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Correo ya existente', 'danger')
            return render_template('auth/register.html', form=form)
        user = User(email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please scan the QR code for 2FA.', 'success')
        login_user(user)  # Iniciar sesión automáticamente después del registro
        return render_template('auth/register.html', form=form, qr_code_url=True)
    return render_template('auth/register.html', form=form, qr_code_url=False)

@auth_bp.route('/qr_code')
@login_required
def qr_code():
    user = current_user
    url = user.get_totp_uri()
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Maneja el inicio de sesión de los usuarios.

    Entradas:
    - Ninguna (obtiene datos del formulario de inicio de sesión).

    Salidas:
    - Redirige al usuario a la página principal si el inicio de sesión es exitoso.
    - Renderiza la plantilla de inicio de sesión con el formulario si hay errores.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('auth.verify_2fa'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/verify_2fa', methods=['GET', 'POST'])
@login_required
def verify_2fa():
    """
    Maneja la doble autenticación de sesión de los usuarios.

    Entradas:
    - Ninguna (obtiene datos del formulario de TwoFactorForm).

    Salidas:
    - Redirige al usuario a la página listado de documentos.
    """
    form = TwoFactorForm()
    if form.validate_on_submit():
        if current_user.verify_totp(form.otp.data):
            current_user.is_authenticated_2fa = True
            db.session.commit()
            return redirect(url_for('documents.list'))
        else:
            flash('Invalid OTP', 'danger')
    return render_template('auth/verify_2fa.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Maneja el cierre de sesión de los usuarios.

    Entradas:
    - Ninguna.

    Salidas:
    - Redirige al usuario a la página de inicio de sesión.
    """
    current_user.is_authenticated_2fa = False
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))