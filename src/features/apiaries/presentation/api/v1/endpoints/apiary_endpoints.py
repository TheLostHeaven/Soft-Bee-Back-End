from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from src.features.apiaries.application.use_cases.create_apiary import CreateApiary
from src.features.apiaries.application.use_cases.get_apiary_by_id import GetApiaryById
from src.features.apiaries.application.use_cases.get_all_apiaries import GetAllApiaries
from src.features.apiaries.application.use_cases.get_apiaries_by_user_id import GetApiariesByUserId
from src.features.apiaries.application.use_cases.update_apiary import UpdateApiary
from src.features.apiaries.application.use_cases.delete_apiary import DeleteApiary
from src.features.apiaries.presentation.api.v1.schemas.apiary_schemas import (
    ApiaryResponseSchema, CreateApiaryRequestSchema, UpdateApiaryRequestSchema
)
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError, ApiaryAlreadyExistsError
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
def create_apiary_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST

        create_request = CreateApiaryRequestSchema(**data)
        create_apiary_use_case: CreateApiary = current_app.container.create_apiary_use_case()
        
        apiary_dto = create_apiary_use_case.execute(create_request)
        return jsonify(ApiaryResponseSchema.model_validate(apiary_dto).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ApiaryAlreadyExistsError as e:
        return jsonify({"message": str(e)}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("", methods=['GET'])
def get_all_apiaries_endpoint():
    try:
        try:
            params = PaginationParams.from_query_args(request.args)
        except ValueError as e:
            return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST

        get_all_apiaries_use_case: GetAllApiaries = current_app.container.get_all_apiaries_use_case()
        page = get_all_apiaries_use_case.execute_paginated(params.limit, params.offset)
        return jsonify(_page_to_json(page)), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['GET'])
def get_apiary_by_id_endpoint(apiary_id: str):
    try:
        get_apiary_by_id_use_case: GetApiaryById = current_app.container.get_apiary_by_id_use_case()
        apiary_dto = get_apiary_by_id_use_case.execute(apiary_id)
        return jsonify(ApiaryResponseSchema.model_validate(apiary_dto).model_dump()), HTTPStatus.OK
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/user/<string:user_id>", methods=['GET'])
def get_apiaries_by_user_id_endpoint(user_id: str):
    try:
        try:
            params = PaginationParams.from_query_args(request.args)
        except ValueError as e:
            return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST

        get_apiaries_by_user_id_use_case: GetApiariesByUserId = current_app.container.get_apiaries_by_user_id_use_case()
        page = get_apiaries_by_user_id_use_case.execute_paginated(user_id, params.limit, params.offset)
        return jsonify(_page_to_json(page)), HTTPStatus.OK
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['PUT'])
def update_apiary_endpoint(apiary_id: str):
    try:
        data = request.json
        if not data:
            return jsonify({"message": "Request body cannot be empty"}), HTTPStatus.BAD_REQUEST
            
        update_request = UpdateApiaryRequestSchema(**data)
        update_apiary_use_case: UpdateApiary = current_app.container.update_apiary_use_case()
        
        apiary_dto = update_apiary_use_case.execute(apiary_id, update_request)
        return jsonify(ApiaryResponseSchema.model_validate(apiary_dto).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@apiaries_bp.route("/<string:apiary_id>", methods=['DELETE'])
def delete_apiary_endpoint(apiary_id: str):
    try:
        delete_apiary_use_case: DeleteApiary = current_app.container.delete_apiary_use_case()
        delete_apiary_use_case.execute(apiary_id)
        return jsonify({}), HTTPStatus.NO_CONTENT
    except ApiaryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
