from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from auth_module.models import User, db
from auth_module.forms import LoginForm, RegisterForm, TwoFactorForm
from auth_module.utils import send_email

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.two_factor_secret:
                return redirect(url_for('auth.verify_2fa'))
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        user.two_factor_secret = pyotp.random_base32()
        db.session.add(user)
        db.session.commit()
        send_email(user.email, 'Activate Your Account', 'auth/verify_2fa', user=user)
        flash('Please check your email to verify your account.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/verify_2fa', methods=['GET', 'POST'])
@login_required
def verify_2fa():
    form = TwoFactorForm()
    if form.validate_on_submit():
        if current_user.verify_totp(form.token.data):
            current_user.is_approved = True
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('Invalid 2FA token')
    return render_template('verify_2fa.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
