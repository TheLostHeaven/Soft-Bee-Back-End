from flask import Blueprint

beehive_bp = Blueprint(
    'beehive',
    __name__,
    url_prefix='/api/v1/beehive'
)

# Importar rutas
from . import routes

__all__ = ['beehive_bp']
