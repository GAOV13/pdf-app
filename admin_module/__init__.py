from flask import Blueprint

# Crear el Blueprint para el módulo de autenticación
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Importar las rutas después de definir el Blueprint para evitar el ciclo
from . import routes