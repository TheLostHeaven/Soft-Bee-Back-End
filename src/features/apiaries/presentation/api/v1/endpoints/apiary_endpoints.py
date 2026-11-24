from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_apiaries_by_user_id import GetApiariesByUserId
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary
from src.features.apiaries.presentation.api.v1.schemas.apiary_schemas import (
    ApiaryResponseSchema, CreateApiaryRequestSchema, UpdateApiaryRequestSchema
)
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError, ApiaryAlreadyExistsError
from src.features.auth.presentation.api.v1.dependencies.auth_deps import token_required
from src.core.authorization import (
    ForbiddenError, ensure_apiary_owner, ensure_same_user, get_authenticated_user_id
)
from pydantic import ValidationError
from src.core.pagination import PaginationParams

apiaries_bp = Blueprint('apiaries_bp', __name__, url_prefix='/api/v1/apiaries')

def _page_to_json(page) -> dict:
    return {
        "items": [ApiaryResponseSchema.model_validate(apiary).model_dump(mode="json") for apiary in page.items],
        "total": page.total,
        "limit": page.limit,
        "offset": page.offset,
    }

@apiaries_bp.route("", methods=['POST'])
@token_required()
def create_apiary_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST

        create_request = CreateApiaryRequestSchema(**data)
        # Solo se pueden crear apiarios para la propia cuenta
        ensure_same_user(create_request.user_id)

        create_apiary_use_case: CreateApiary = current_app.container.create_apiary_use_case()

        apiary_dto = create_apiary_use_case.execute(create_request)
        return jsonify(ApiaryResponseSchema.model_validate(apiary_dto).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryAlreadyExistsError as e:
        return jsonify({"message": str(e)}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("", methods=['GET'])
@token_required()
def get_all_apiaries_endpoint():
    """Devuelve los apiarios del usuario autenticado (paginado)."""
    try:
        try:
            params = PaginationParams.from_query_args(request.args)
        except ValueError as e:
            return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST

        user_id = get_authenticated_user_id()
        use_case: GetApiariesByUserId = current_app.container.get_apiaries_by_user_id_use_case()
        page = use_case.execute_paginated(user_id, params.limit, params.offset)
        return jsonify(_page_to_json(page)), HTTPStatus.OK
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['GET'])
@token_required()
def get_apiary_by_id_endpoint(apiary_id: str):
    try:
        apiary_dto = ensure_apiary_owner(apiary_id)
        return jsonify(ApiaryResponseSchema.model_validate(apiary_dto).model_dump()), HTTPStatus.OK
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/user/<string:user_id>", methods=['GET'])
@token_required()
def get_apiaries_by_user_id_endpoint(user_id: str):
    try:
        # Solo se pueden consultar los apiarios de la propia cuenta
        ensure_same_user(user_id)

        try:
            params = PaginationParams.from_query_args(request.args)
        except ValueError as e:
            return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST

        get_apiaries_by_user_id_use_case: GetApiariesByUserId = current_app.container.get_apiaries_by_user_id_use_case()
        page = get_apiaries_by_user_id_use_case.execute_paginated(user_id, params.limit, params.offset)
        return jsonify(_page_to_json(page)), HTTPStatus.OK
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['PUT'])
@token_required()
def update_apiary_endpoint(apiary_id: str):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST

        update_request = UpdateApiaryRequestSchema(**data)
        ensure_apiary_owner(apiary_id)

        update_apiary_use_case: UpdateApiary = current_app.container.update_apiary_use_case()

        apiary_dto = update_apiary_use_case.execute(apiary_id, update_request)
        return jsonify(ApiaryResponseSchema.model_validate(apiary_dto).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['DELETE'])
@token_required()
def delete_apiary_endpoint(apiary_id: str):
    try:
        ensure_apiary_owner(apiary_id)

        delete_apiary_use_case: DeleteApiary = current_app.container.delete_apiary_use_case()
        delete_apiary_use_case.execute(apiary_id)
        return jsonify({}), HTTPStatus.NO_CONTENT
    except ForbiddenError as e:
        return jsonify({"message": str(e)}), HTTPStatus.FORBIDDEN
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
