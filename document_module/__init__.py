from flask import Blueprint

document_bp = Blueprint('documents', __name__, template_folder='templates')

from . import routes