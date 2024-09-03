from app import app
from auth_module.models import db

with app.app_context():
    db.create_all()
    print("Database initialized!")