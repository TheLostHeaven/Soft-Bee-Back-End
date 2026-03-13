from flask import Blueprint

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/v1/statistics')

from src.features.statistics.presentation.api.v1.endpoints import routes
