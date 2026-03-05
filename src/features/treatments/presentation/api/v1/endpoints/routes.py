from flask import request, jsonify, current_app
from http import HTTPStatus
from uuid import UUID
from pydantic import ValidationError

from src.features.treatments.presentation.api.v1.endpoints import treatments_bp
from src.features.treatments.presentation.api.v1.schemas.treatment_schemas import (
    CreateTreatmentRequestSchema, UpdateTreatmentRequestSchema, TreatmentResponseSchema,
    CreateFollowupRequestSchema, UpdateFollowupRequestSchema, FollowupResponseSchema
)
from src.features.treatments.application.use_cases.create_treatment import CreateTreatmentUseCase
from src.features.treatments.application.use_cases.get_treatments import GetTreatmentsByHiveUseCase
from src.features.treatments.application.use_cases.get_treatment_by_id import GetTreatmentByIdUseCase
from src.features.treatments.application.use_cases.update_treatment import UpdateTreatmentUseCase
from src.features.treatments.application.use_cases.delete_treatment import DeleteTreatmentUseCase
from src.features.treatments.application.use_cases.create_followup import CreateFollowupUseCase
from src.features.treatments.application.use_cases.update_followup import UpdateFollowupUseCase
from src.features.treatments.application.use_cases.delete_followup import DeleteFollowupUseCase

@treatments_bp.route("", methods=['POST'])
def create_treatment():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        create_request = CreateTreatmentRequestSchema(**data)
        use_case: CreateTreatmentUseCase = current_app.container.create_treatment_use_case()
        
        treatment_dto = use_case.execute(create_request)
        return jsonify(TreatmentResponseSchema.model_validate(treatment_dto).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/<uuid:id>", methods=['GET'])
def get_treatment_by_id(id: UUID):
    try:
        use_case: GetTreatmentByIdUseCase = current_app.container.get_treatment_by_id_use_case()
        treatment_dto = use_case.execute(id)
        if not treatment_dto:
            return jsonify({"message": "Treatment not found"}), HTTPStatus.NOT_FOUND
        return jsonify(TreatmentResponseSchema.model_validate(treatment_dto).model_dump()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/hive/<uuid:hive_id>", methods=['GET'])
def get_treatments_by_hive(hive_id: UUID):
    try:
        use_case: GetTreatmentsByHiveUseCase = current_app.container.get_treatments_by_hive_use_case()
        treatments_dto = use_case.execute(hive_id)
        return jsonify([TreatmentResponseSchema.model_validate(t).model_dump() for t in treatments_dto]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/<uuid:id>", methods=['PUT', 'PATCH'])
def update_treatment(id: UUID):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        update_request = UpdateTreatmentRequestSchema(**data)
        use_case: UpdateTreatmentUseCase = current_app.container.update_treatment_use_case()
        
        treatment_dto = use_case.execute(id, update_request)
        if not treatment_dto:
            return jsonify({"message": "Treatment not found"}), HTTPStatus.NOT_FOUND
        return jsonify(TreatmentResponseSchema.model_validate(treatment_dto).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/<uuid:id>", methods=['DELETE'])
def delete_treatment(id: UUID):
    try:
        use_case: DeleteTreatmentUseCase = current_app.container.delete_treatment_use_case()
        success = use_case.execute(id)
        if not success:
            return jsonify({"message": "Treatment not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"message": "Treatment deleted successfully"}), HTTPStatus.OK
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
        return jsonify(FollowupResponseSchema.model_validate(followup_dto).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/followup/<uuid:followup_id>", methods=['PUT', 'PATCH'])
def update_followup(followup_id: UUID):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        update_request = UpdateFollowupRequestSchema(**data)
        use_case: UpdateFollowupUseCase = current_app.container.update_followup_use_case()
        
        followup_dto = use_case.execute(followup_id, update_request)
        if not followup_dto:
            return jsonify({"message": "Followup not found"}), HTTPStatus.NOT_FOUND
        return jsonify(FollowupResponseSchema.model_validate(followup_dto).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@treatments_bp.route("/followup/<uuid:followup_id>", methods=['DELETE'])
def delete_followup(followup_id: UUID):
    try:
        use_case: DeleteFollowupUseCase = current_app.container.delete_followup_use_case()
        success = use_case.execute(followup_id)
        if not success:
            return jsonify({"message": "Followup not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"message": "Followup deleted successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
