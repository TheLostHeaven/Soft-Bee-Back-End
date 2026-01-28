from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from dependency_injector.wiring import inject, Provide
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_all_apiaries import GetAllApiaries
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary
from src.features.apiaries.presentation.api.v1.schemas.apiary_schemas import (
    ApiaryResponseSchema, CreateApiaryRequestSchema, UpdateApiaryRequestSchema
)
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError, ApiaryAlreadyExistsError, PermissionDeniedException
from pydantic import ValidationError
from src.features.auth.presentation.api.v1.dependencies.auth_deps import token_required, get_current_user_id
from src.core.dependencies.containers import MainContainer as Container


apiaries_bp = Blueprint('apiaries_bp', __name__, url_prefix='/api/v1/apiaries')

@apiaries_bp.route("", methods=['POST'])
@inject
@token_required()
def create_apiary_endpoint(
    create_apiary_use_case: CreateApiary = Provide[Container.create_apiary_use_case]
):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST

        create_request = CreateApiaryRequestSchema(**data)
        
        authenticated_user_id = get_current_user_id()
        apiary_dto = create_apiary_use_case.execute(create_request, authenticated_user_id)
        return jsonify(ApiaryResponseSchema.from_orm(apiary_dto).dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ApiaryAlreadyExistsError as e:
        return jsonify({"message": str(e)}), HTTPStatus.CONFLICT
    except PermissionDeniedException as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("", methods=['GET'])
@inject
@token_required()
def get_all_apiaries_endpoint(
    get_all_apiaries_use_case: GetAllApiaries = Provide[Container.get_all_apiaries_use_case]
):
    try:
        authenticated_user_id = get_current_user_id()
        apiaries_dto = get_all_apiaries_use_case.execute(authenticated_user_id)
        return jsonify([ApiaryResponseSchema.from_orm(apiary).dict() for apiary in apiaries_dto]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['GET'])
@inject
@token_required()
def get_apiary_by_id_endpoint(
    apiary_id: str,
    get_apiary_by_id_use_case: GetApiaryById = Provide[Container.get_apiary_by_id_use_case]
):
    try:
        authenticated_user_id = get_current_user_id()
        apiary_dto = get_apiary_by_id_use_case.execute(apiary_id, authenticated_user_id)
        return jsonify(ApiaryResponseSchema.from_orm(apiary_dto).dict()), HTTPStatus.OK
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except PermissionDeniedException as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['PUT'])
@inject
@token_required()
def update_apiary_endpoint(
    apiary_id: str,
    update_apiary_use_case: UpdateApiary = Provide[Container.update_apiary_use_case]
):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        update_request = UpdateApiaryRequestSchema(**data)
        
        authenticated_user_id = get_current_user_id()
        apiary_dto = update_apiary_use_case.execute(apiary_id, update_request, authenticated_user_id)
        return jsonify(ApiaryResponseSchema.from_orm(apiary_dto).dict()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except PermissionDeniedException as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['DELETE'])
@inject
@token_required()
def delete_apiary_endpoint(
    apiary_id: str,
    delete_apiary_use_case: DeleteApiary = Provide[Container.delete_apiary_use_case]
):
    try:
        authenticated_user_id = get_current_user_id()
        delete_apiary_use_case.execute(apiary_id, authenticated_user_id)
        return jsonify({}), HTTPStatus.NO_CONTENT
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except PermissionDeniedException as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR