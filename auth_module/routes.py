import qrcode
from io import BytesIO
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, db
from .forms import RegistrationForm, LoginForm, TwoFactorForm

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        login_user(user)  # Iniciar sesión automáticamente después del registro
        return redirect(url_for('auth.qr_code'))
    return render_template('auth/register.html', form=form)

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
    current_user.is_authenticated_2fa = False
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))