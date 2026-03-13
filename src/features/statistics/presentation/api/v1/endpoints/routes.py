from flask import request, jsonify, current_app
from http import HTTPStatus
from uuid import UUID
from datetime import datetime
from src.features.statistics.presentation.api.v1.endpoints import statistics_bp
from src.features.statistics.presentation.api.v1.schemas.statistics_schemas import (
    ApiaryStatisticsSchema,
    BeehiveHealthTrendSchema,
    TreatmentDistributionSchema,
    InventoryLevelSchema,
    AnswerScoreTrendSchema
)

@statistics_bp.route("/apiary/<string:apiary_id>", methods=['GET'])
def get_apiary_statistics(apiary_id: str):
    """Obtiene estadísticas generales de un apiario"""
    try:
        use_case = current_app.container.get_apiary_statistics_use_case()
        stats = use_case.execute(UUID(apiary_id))
        
        if not stats:
            return jsonify({"message": "Apiary not found or no data available"}), HTTPStatus.NOT_FOUND
        
        return jsonify(ApiaryStatisticsSchema.model_validate(stats).model_dump(mode='json')), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@statistics_bp.route("/apiary/<string:apiary_id>/health-trends", methods=['GET'])
def get_beehive_health_trends(apiary_id: str):
    """Obtiene tendencias de salud de colmenas"""
    try:
        # Query params para filtrar por fecha
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None
        
        use_case = current_app.container.get_beehive_health_trends_use_case()
        trends = use_case.execute(UUID(apiary_id), start_date, end_date)
        
        return jsonify([BeehiveHealthTrendSchema.model_validate(t).model_dump() for t in trends]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@statistics_bp.route("/apiary/<string:apiary_id>/treatment-distribution", methods=['GET'])
def get_treatment_distribution(apiary_id: str):
    """Obtiene distribución de tratamientos (para gráfico de pie/dona)"""
    try:
        use_case = current_app.container.get_treatment_distribution_use_case()
        distribution = use_case.execute(UUID(apiary_id))
        
        return jsonify([TreatmentDistributionSchema.model_validate(d).model_dump() for d in distribution]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@statistics_bp.route("/apiary/<string:apiary_id>/inventory-levels", methods=['GET'])
def get_inventory_levels(apiary_id: str):
    """Obtiene niveles de inventario (para gráfico de barras)"""
    try:
        use_case = current_app.container.get_inventory_levels_use_case()
        levels = use_case.execute(UUID(apiary_id))
        
        return jsonify([InventoryLevelSchema.model_validate(l).model_dump() for l in levels]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@statistics_bp.route("/apiary/<string:apiary_id>/answer-score-trends", methods=['GET'])
def get_answer_score_trends(apiary_id: str):
    """Obtiene tendencias de scores de respuestas por categoría (para gráfico de líneas)"""
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None
        
        use_case = current_app.container.get_answer_score_trends_use_case()
        trends = use_case.execute(UUID(apiary_id), start_date, end_date)
        
        return jsonify([AnswerScoreTrendSchema.model_validate(t).model_dump() for t in trends]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
