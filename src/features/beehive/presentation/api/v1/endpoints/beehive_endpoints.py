from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from src.features.beehive.application.use_cases.create_beehive import CreateBeehiveUseCase
from src.features.beehive.application.use_cases.get_all_beehives_by_apiary_id import GetAllBeehivesByApiaryIdUseCase
from src.features.beehive.application.use_cases.update_beehive import UpdateBeehiveUseCase
from src.features.beehive.application.use_cases.delete_beehive import DeleteBeehiveUseCase
from src.features.beehive.presentation.api.v1.schemas.beehive_schemas import (
    BeehiveResponseSchema, CreateBeehiveRequestSchema, UpdateBeehiveRequestSchema
)
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException, DuplicateHiveNumberException
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError
from src.features.auth.presentation.api.v1.dependencies.auth_deps import token_required
from src.core.authorization import ForbiddenError, ensure_apiary_owner, ensure_hive_owner
from pydantic import ValidationError
from uuid import UUID
from src.core.pagination import PaginationParams

beehive_bp = Blueprint('beehive_bp', __name__, url_prefix='/api/v1/beehives')

@beehive_bp.route("", methods=['POST'])
@token_required()
def create_beehive_endpoint():
    try:
        data = request.json
        if not data: return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST

        create_request = CreateBeehiveRequestSchema(**data)
        # Solo se pueden crear colmenas en apiarios propios
        ensure_apiary_owner(create_request.apiary_id)

        create_beehive_use_case: CreateBeehiveUseCase = current_app.container.create_beehive_use_case()
        
        beehive_dto = create_beehive_use_case.execute(create_request)
        return jsonify(BeehiveResponseSchema.model_validate(beehive_dto).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except DuplicateHiveNumberException as e:
        return jsonify({"message": str(e)}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/<uuid:id>", methods=['GET'])
@token_required()
def get_beehive_by_id_endpoint(id: UUID):
    try:
        beehive_dto = ensure_hive_owner(id)
        return jsonify(BeehiveResponseSchema.model_validate(beehive_dto).model_dump()), HTTPStatus.OK
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except BeehiveNotFoundException as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/apiary/<uuid:apiary_id>", methods=['GET'])
@token_required()
def get_all_beehives_by_apiary_id_endpoint(apiary_id: UUID):
    try:
        try:
            params = PaginationParams.from_query_args(request.args)
        except ValueError as e:
            return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST

        ensure_apiary_owner(apiary_id)

        get_all_beehives_by_apiary_id_use_case: GetAllBeehivesByApiaryIdUseCase = current_app.container.get_all_beehives_by_apiary_id_use_case()
        page = get_all_beehives_by_apiary_id_use_case.execute_paginated(apiary_id, params.limit, params.offset)
        return jsonify({
            "items": [BeehiveResponseSchema.model_validate(beehive).model_dump(mode="json") for beehive in page.items],
            "total": page.total,
            "limit": page.limit,
            "offset": page.offset,
        }), HTTPStatus.OK
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/<uuid:id>", methods=['PUT'])
@token_required()
def update_beehive_endpoint(id: UUID):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        update_request = UpdateBeehiveRequestSchema(**data)
        ensure_hive_owner(id)

        update_beehive_use_case: UpdateBeehiveUseCase = current_app.container.update_beehive_use_case()
        
        beehive_dto = update_beehive_use_case.execute(id, update_request)
        return jsonify(BeehiveResponseSchema.model_validate(beehive_dto).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except BeehiveNotFoundException as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@beehive_bp.route("/<uuid:id>", methods=['DELETE'])
@token_required()
def delete_beehive_endpoint(id: UUID):
    try:
        ensure_hive_owner(id)

        delete_beehive_use_case: DeleteBeehiveUseCase = current_app.container.delete_beehive_use_case()
        delete_beehive_use_case.execute(id)
        return jsonify({}), HTTPStatus.NO_CONTENT
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except BeehiveNotFoundException as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
