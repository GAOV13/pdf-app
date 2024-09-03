from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from auth_module.models import User
from auth_module.routes import auth_bp

app = Flask(__name__)
app.config.from_object('config.Config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
