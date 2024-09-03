from flask import Flask
from config import Config
from auth_module.models import db, User
from auth_module.routes import auth_bp
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

# Registrar el blueprint de autenticación
app.register_blueprint(auth_bp, url_prefix='/auth')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)  # Inicializar LoginManager con la aplicación
login_manager.login_view = 'auth.login'

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)