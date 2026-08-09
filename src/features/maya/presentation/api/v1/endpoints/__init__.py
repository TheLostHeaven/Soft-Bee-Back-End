from flask import Blueprint

maya_bp = Blueprint(
    'maya',
    __name__,
    url_prefix='/api/v1/maya'
)

from . import routes

__all__ = ['maya_bp']
