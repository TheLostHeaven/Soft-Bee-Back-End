from flask import Blueprint, request, jsonify, current_app
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError
from .....application.dto.auth_dto import (
    LoginRequestDTO, RegisterRequestDTO, RefreshTokenRequestDTO,
    LogoutRequestDTO, VerifyTokenRequestDTO, RegisterResponseDTO
)
from .....application.use_cases.login_user import LoginUserUseCase
from .....application.use_cases.register_user import RegisterUserUseCase
# from .....application.use_cases.refresh_token import RefreshTokenUseCase
# from .....application.use_cases.logout_user import LogoutUserUseCase
# from .....application.use_cases.verify_token import VerifyTokenUseCase
from src.core.dependencies.containers import MainContainer as Container
from ..schemas.auth_schemas import (
    LoginSchema, RegisterSchema, RefreshTokenSchema,
    LogoutSchema, VerifyTokenSchema, AuthResponseSchema
)

# Crear blueprint para auth v1
auth_bp = Blueprint('auth_v1', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
@inject
def login(
    login_use_case: LoginUserUseCase = Provide[Container.login_use_case]
):
    """Login de usuario"""
    try:
        # Validar input con Pydantic
        validated_data = LoginSchema(**request.json)
        data = validated_data.model_dump()
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    # Convertir a DTO
    login_request = LoginRequestDTO(**data)
    
    # Ejecutar caso de uso
    result, error = login_use_case.execute(login_request)
    
    if error:
        return jsonify({"error": error}), 401
    
    # Serializar respuesta con Pydantic
    response_data = AuthResponseSchema.model_validate(result, from_attributes=True)
    return jsonify(response_data.model_dump()), 200

@auth_bp.route('/register', methods=['POST'])
@inject
def register(
    register_use_case: RegisterUserUseCase = Provide[Container.register_use_case]
):
    """Registro de usuario"""
    try:
        # Validar input con Pydantic
        validated_data = RegisterSchema(**request.json)
        # Pasar todos los datos validados, incluyendo 'confirm_password'
        data_for_dto = validated_data.model_dump()
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    register_request = RegisterRequestDTO(**data_for_dto)
    
    result, error = register_use_case.execute(register_request)
    
    if error:
        return jsonify({"error": error}), 400
    
    # Return the full RegisterResponseDTO
    return jsonify(result.model_dump()), 201

# @auth_bp.route('/refresh', methods=['POST'])
# @inject
# def refresh_token(
#     refresh_use_case: RefreshTokenUseCase = Provide[Container.refresh_token_use_case]
# ):
#     """Refresh token"""
#     schema = RefreshTokenSchema()
#     try:
#         data = schema.load(request.json)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    
#     refresh_request = RefreshTokenRequestDTO(**data)
    
#     result, error = refresh_use_case.execute(refresh_request)
    
#     if error:
#         return jsonify({"error": error}), 401
    
#     return jsonify({
#         "access_token": result.access_token,
#         "refresh_token": result.refresh_token,
#         "token_type": result.token_type,
#         "expires_in": result.expires_in
#     }), 200

# @auth_bp.route('/logout', methods=['POST'])
# @inject
# def logout(
#     logout_use_case: LogoutUserUseCase = Provide[Container.logout_use_case]
# ):
#     """Logout de usuario"""
#     schema = LogoutSchema()
#     try:
#         data = schema.load(request.json)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    
#     logout_request = LogoutRequestDTO(**data)
    
#     success, error = logout_use_case.execute(logout_request)
    
#     if error:
#         return jsonify({"error": error}), 400
    
#     return jsonify({"message": "Logged out successfully"}), 200

# @auth_bp.route('/verify', methods=['POST'])
# @inject
# def verify_token(
#     verify_use_case: VerifyTokenUseCase = Provide[Container.verify_token_use_case]
# ):
#     """Verificar token"""
#     schema = VerifyTokenSchema()
#     try:
#         data = schema.load(request.json)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    
#     verify_request = VerifyTokenRequestDTO(**data)
    
#     result, error = verify_use_case.execute(verify_request)
    
#     if error:
#         return jsonify({"error": error}), 401
    
#     return jsonify({
#         "is_valid": result.is_valid,
#         "user_id": result.user_id,
#         "email": result.email,
#         "expires_at": result.expires_at.isoformat() if result.expires_at else None
#     }), 200

@auth_bp.route('/health', methods=['GET'])
def auth_health():
    """Health check para feature auth"""
    return jsonify({
        "status": "healthy",
        "feature": "auth",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            # "/api/v1/auth/refresh",
            "/api/v1/auth/logout",
            "/api/v1/auth/verify"
        ]
    })