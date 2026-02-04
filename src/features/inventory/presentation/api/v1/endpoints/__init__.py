from flask import Blueprint

inventory_bp = Blueprint(
    'inventory',
    __name__,
    url_prefix='/api/v1/inventory'
)

# Importar rutas
from . import routes

__all__ = ['inventory_bp']
