from flask import Blueprint

questions_bp = Blueprint(
    'questions',
    __name__,
    url_prefix='/api/v1/questions'
)

# Importar rutas
from . import routes

__all__ = ['questions_bp']
