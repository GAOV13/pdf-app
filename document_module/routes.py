from flask import render_template, redirect, url_for, flash, request, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import document_bp
from .models import db, Document
from .forms import CreateDocumentForm, UpdateDocumentForm
from auth_module.models import User
import random

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@document_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = CreateDocumentForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            admins = User.query.all()
            approver = random.choice(admins)
            document = Document(
                title=form.title.data,
                description=form.description.data,
                file_path=file_path,
                uploaded_by=current_user.id,
                approved_by=approver.id
            )
            db.session.add(document)
            db.session.commit()
            flash('Document uploaded successfully', 'success')
            return redirect(url_for('documents.list'))
    return render_template('documents/upload.html', form=form)

@document_bp.route('/list')
@login_required
def list():
    documents = Document.query.filter_by(uploaded_by=current_user.id).all()
    return render_template('documents/list.html', documents=documents)

@document_bp.route('/edit/<int:document_id>', methods=['GET', 'POST'])
@login_required
def edit(document_id):
    document = Document.query.get_or_404(document_id)
    if document.uploaded_by != current_user.id:
        flash('You are not authorized to edit this document', 'danger')
        return redirect(url_for('documents.list'))
    form = UpdateDocumentForm(obj=document)
    if form.validate_on_submit():
        document.title = form.title.data
        document.description = form.description.data
        db.session.commit() 
        flash('Document updated successfully', 'success')
        return redirect(url_for('documents.list'))
    else:
        print("")
        print(form.errors)
    return render_template('documents/edit.html', form=form, document=document)

@document_bp.route('/delete/<int:document_id>', methods=['POST'])
@login_required
def delete(document_id):
    document = Document.query.get_or_404(document_id)
    if document.uploaded_by != current_user.id:
        flash('You are not authorized to delete this document', 'danger')
        return redirect(url_for('documents.list'))
    # Eliminar el archivo del sistema de archivos
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], document.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Eliminar el documento de la base de datos
    db.session.delete(document)
    db.session.commit()
    flash('Document deleted successfully', 'success')
    return redirect(url_for('documents.list'))

@document_bp.route('/preview/<int:document_id>', methods=['GET'])
@login_required
def preview(document_id):
    document = Document.query.get_or_404(document_id)
    if document.uploaded_by != current_user.id:
        flash('You are not authorized to view this document', 'danger')
        return redirect(url_for('documents.list'))
    documents = Document.query.filter_by(uploaded_by=current_user.id).all()
    return render_template('documents/list.html', documents=documents, selected_document=document)

@document_bp.route('/serve_file/<int:document_id>')
@login_required
def serve_file(document_id):
    document = Document.query.get_or_404(document_id)
    filename = os.path.basename(document.file_path)
    return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], path=filename, as_attachment=False)