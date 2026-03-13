from flask import request, jsonify, current_app
from http import HTTPStatus
from uuid import UUID
from pydantic import ValidationError

from src.features.treatments.presentation.api.v1.endpoints import treatments_bp
from src.features.treatments.presentation.api.v1.schemas.treatment_schemas import (
    CreateTreatmentRequestSchema, TreatmentResponseSchema,
    CreateFollowupRequestSchema, FollowupResponseSchema
)
from src.features.treatments.application.use_cases.create_treatment import CreateTreatmentUseCase
from src.features.treatments.application.use_cases.get_treatments import GetTreatmentsByHiveUseCase
from src.features.treatments.application.use_cases.create_followup import CreateFollowupUseCase

@treatments_bp.route("", methods=['POST'])
def create_treatment():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        create_request = CreateTreatmentRequestSchema(**data)
        use_case: CreateTreatmentUseCase = current_app.container.create_treatment_use_case()
        
        treatment_dto = use_case.execute(create_request)
        return jsonify(TreatmentResponseSchema.model_validate(treatment_dto).model_dump(mode='json')), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/hive/<uuid:hive_id>", methods=['GET'])
def get_treatments_by_hive(hive_id: UUID):
    try:
        use_case: GetTreatmentsByHiveUseCase = current_app.container.get_treatments_by_hive_use_case()
        treatments_dto = use_case.execute(hive_id)
        return jsonify([TreatmentResponseSchema.model_validate(t).model_dump(mode='json') for t in treatments_dto]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/followup", methods=['POST'])
def create_followup():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        create_request = CreateFollowupRequestSchema(**data)
        use_case: CreateFollowupUseCase = current_app.container.create_followup_use_case()
        
        followup_dto = use_case.execute(create_request)
        return jsonify(FollowupResponseSchema.model_validate(followup_dto).model_dump(mode='json')), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
