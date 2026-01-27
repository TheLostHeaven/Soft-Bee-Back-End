from flask import Blueprint

user_bp = Blueprint(
    'user',
    __name__,
    url_prefix='/api/v1/user'
)

# Importar rutas
from . import routes

__all__ = ['user_bp']
