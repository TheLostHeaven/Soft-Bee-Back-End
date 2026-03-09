from flask import Blueprint

answers_bp = Blueprint(
    'answers',
    __name__,
    url_prefix='/api/v1/answers'
)

from . import routes

__all__ = ['answers_bp']
