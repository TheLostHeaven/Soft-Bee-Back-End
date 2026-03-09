from flask import Blueprint

answer_bp = Blueprint(
    'answer',
    __name__,
    url_prefix='/api/v1/answer'
)

# Importar rutas
from . import routes

__all__ = ['answer_bp']
