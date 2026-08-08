from flask import Blueprint, jsonify, current_app
from http import HTTPStatus
from uuid import UUID
from src.features.reports.application.use_cases.generate_apiary_report import GenerateApiaryReport
from src.features.reports.application.dto.apiary_report_dto import ApiaryReportDto
from pydantic import ValidationError

reports_bp = Blueprint('reports_bp', __name__, url_prefix='/api/v1/reports')


@reports_bp.route("/apiary/<uuid:apiary_id>", methods=['GET'])
def get_apiary_report(apiary_id: UUID):
    """
    Endpoint para obtener un reporte completo del apiario
    
    Incluye:
    - Información básica del apiario
    - Inventario completo
    - Todas las colmenas con:
        - Datos de la colmena
        - Preguntas y respuestas asociadas
    - Estadísticas: total de preguntas y respuestas
    """
    try:
        generate_report_use_case: GenerateApiaryReport = current_app.container.generate_apiary_report_use_case()
        report_dto = generate_report_use_case.execute(apiary_id)
        
        # Convertir el DTO a dict para la respuesta JSON
        return jsonify(ApiaryReportDto.model_validate(report_dto).model_dump()), HTTPStatus.OK
    except ValueError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": f"Error al generar el reporte: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR
