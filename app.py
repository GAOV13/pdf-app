from flask import Flask
from config import Config
from auth_module.models import db, User
from document_module.models import Document
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    """
    Carga un usuario dado su ID.

    Entradas:
    - user_id (int): ID del usuario.

    Salidas:
    - User: Objeto de usuario correspondiente al ID.
    """
    return User.query.get(int(user_id))

# Registrar el blueprint de autenticación
from auth_module.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# Registrar el blueprint de documentos
from document_module.routes import document_bp
app.register_blueprint(document_bp, url_prefix='/documents')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document}

if __name__ == '__main__':
    app.run(debug=True)