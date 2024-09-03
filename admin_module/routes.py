from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Admin, db
from .forms import AdminLoginForm
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('users.admin_dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@admin_bp.route('/admin', methods=['GET'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/admin/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    if not current_user.is_admin:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(original_username=user.username, original_email=user.email, obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('users.admin_dashboard'))
    return render_template('edit_profile.html', form=form, user=user)

@admin_bp.route('/admin/make_admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash('You are not authorized to perform this action', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash('User has been made an admin', 'success')
    return redirect(url_for('users.admin_dashboard'))