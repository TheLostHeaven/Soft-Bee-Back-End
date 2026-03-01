from flask import Blueprint

treatments_bp = Blueprint(
    'treatments',
    __name__,
    url_prefix='/api/v1/treatments'
)

# Importar rutas
from . import routes

__all__ = ['treatments_bp']
