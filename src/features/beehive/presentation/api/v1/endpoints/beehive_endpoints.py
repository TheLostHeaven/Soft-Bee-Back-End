from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from src.features.beehive.application.use_cases.create_beehive import CreateBeehiveUseCase
from src.features.beehive.application.use_cases.get_beehive_by_id import GetBeehiveByIdUseCase
from src.features.beehive.application.use_cases.get_all_beehives_by_apiary_id import GetAllBeehivesByApiaryIdUseCase
from src.features.beehive.application.use_cases.update_beehive import UpdateBeehiveUseCase
from src.features.beehive.application.use_cases.delete_beehive import DeleteBeehiveUseCase
from src.features.beehive.presentation.api.v1.schemas.beehive_schemas import (
    BeehiveResponseSchema, CreateBeehiveRequestSchema, UpdateBeehiveRequestSchema
)
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException
from pydantic import ValidationError
from uuid import UUID

beehive_bp = Blueprint('beehive_bp', __name__, url_prefix='/api/v1/beehives')

@beehive_bp.route("", methods=['POST'])
def create_beehive_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST

        create_request = CreateBeehiveRequestSchema(**data)
        create_beehive_use_case: CreateBeehiveUseCase = current_app.container.create_beehive_use_case()
        
        beehive_dto = create_beehive_use_case.execute(create_request)
        return jsonify(BeehiveResponseSchema.from_orm(beehive_dto).dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/<uuid:beehive_id>", methods=['GET'])
def get_beehive_by_id_endpoint(beehive_id: UUID):
    try:
        get_beehive_by_id_use_case: GetBeehiveByIdUseCase = current_app.container.get_beehive_by_id_use_case()
        beehive_dto = get_beehive_by_id_use_case.execute(beehive_id)
        return jsonify(BeehiveResponseSchema.from_orm(beehive_dto).dict()), HTTPStatus.OK
    except BeehiveNotFoundException as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/apiary/<uuid:apiary_id>", methods=['GET'])
def get_all_beehives_by_apiary_id_endpoint(apiary_id: UUID):
    try:
        get_all_beehives_by_apiary_id_use_case: GetAllBeehivesByApiaryIdUseCase = current_app.container.get_all_beehives_by_apiary_id_use_case()
        beehives_dto = get_all_beehives_by_apiary_id_use_case.execute(apiary_id)
        return jsonify([BeehiveResponseSchema.from_orm(beehive).dict() for beehive in beehives_dto]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/<uuid:beehive_id>", methods=['PUT'])
def update_beehive_endpoint(beehive_id: UUID):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        update_request = UpdateBeehiveRequestSchema(**data)
        update_beehive_use_case: UpdateBeehiveUseCase = current_app.container.update_beehive_use_case()
        
        beehive_dto = update_beehive_use_case.execute(beehive_id, update_request)
        return jsonify(BeehiveResponseSchema.from_orm(beehive_dto).dict()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except BeehiveNotFoundException as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/<uuid:beehive_id>", methods=['DELETE'])
def delete_beehive_endpoint(beehive_id: UUID):
    try:
        delete_beehive_use_case: DeleteBeehiveUseCase = current_app.container.delete_beehive_use_case()
        delete_beehive_use_case.execute(beehive_id)
        return jsonify({}), HTTPStatus.NO_CONTENT
    except BeehiveNotFoundException as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
