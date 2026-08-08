from flask import Blueprint

charts_bp = Blueprint(
    'charts',
    __name__,
    url_prefix='/api/v1/charts'
)

# Importar rutas
from . import routes

__all__ = ['charts_bp']
