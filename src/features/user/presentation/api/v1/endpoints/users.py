from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError
from uuid import UUID

from src.features.user.application.use_cases.get_user import GetUserUseCase
from src.features.user.application.use_cases.update_user import UpdateUserUseCase
from src.features.user.application.use_cases.delete_user import DeleteUserUseCase
from src.features.user.application.dto.user_dto import UpdateUserDTO
from src.features.user.presentation.api.v1.schemas.user_schemas import UpdateUserSchema
from src.core.dependencies.containers import MainContainer

user_bp = Blueprint('user_v1', __name__, url_prefix='/api/v1/users')

@user_bp.route('/<uuid:user_id>', methods=['GET'])
@inject
def get_user(
    user_id: UUID,
    get_user_use_case: GetUserUseCase = Provide[MainContainer.get_user_use_case]
):
    try:
        user = get_user_use_case.execute(user_id)
        if user:
            return jsonify(user.model_dump()), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<uuid:user_id>', methods=['PUT'])
@inject
def update_user(
    user_id: UUID,
    update_user_use_case: UpdateUserUseCase = Provide[MainContainer.update_user_use_case]
):
    try:
        schema = UpdateUserSchema(**request.json)
        update_dto = UpdateUserDTO(
            username=schema.username,
            email=schema.email,
            first_name=schema.first_name,
            last_name=schema.last_name,
            phone=schema.phone
        )
        user = update_user_use_case.execute(user_id, update_dto)
        if user:
            return jsonify(user.model_dump()), 200
        return jsonify({"error": "User not found"}), 404
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
@inject
def delete_user(
    user_id: UUID,
    delete_user_use_case: DeleteUserUseCase = Provide[MainContainer.delete_user_use_case]
):
    try:
        delete_user_use_case.execute(user_id)
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
