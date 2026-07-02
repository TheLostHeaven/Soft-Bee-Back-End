from flask import Blueprint, request, jsonify, current_app
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError

# Importar DTOs existentes
from src.features.auth.application.dto.auth_dto import (
    LoginRequestDTO, RegisterRequestDTO, RefreshTokenRequestDTO,
    LogoutRequestDTO, VerifyTokenRequestDTO, RegisterResponseDTO
)

# Importar DTOs para reset password
from src.features.auth.application.dto.reset_password_dto import (
    ResetPasswordConfirmDTO,
    ForgotPasswordRequestDTO
)

# Importar casos de uso existentes
from src.features.auth.application.use_cases.login_user import LoginUserUseCase
from src.features.auth.application.use_cases.register_user import RegisterUserUseCase
from src.features.auth.application.errors import AuthErrorCode, build_auth_error
# from src.features.auth.application.use_cases.refresh_token import RefreshTokenUseCase
# from src.features.auth.application.use_cases.logout_user import LogoutUserUseCase
# from src.features.auth.application.use_cases.verify_token import VerifyTokenUseCase

# Importar nuevos casos de uso para reset password
from src.features.auth.application.use_cases.forgot_password import ForgotPasswordUseCase
from src.features.auth.application.use_cases.reset_password import ResetPasswordUseCase

# Importar container DI
from src.core.dependencies.containers import MainContainer

# Importar schemas existentes
from src.features.auth.presentation.api.v1.schemas.auth_schemas import (
    LoginSchema, RegisterSchema, AuthResponseSchema
)

# Importar schemas para reset password
from src.features.auth.presentation.api.v1.schemas.auth_schemas import (
    ForgotPasswordSchema,
    ResetPasswordSchema,
    ResetPasswordResponseSchema,
)

auth_bp = Blueprint('auth_v1', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
@inject
def login(
    login_use_case: LoginUserUseCase = Provide[MainContainer.login_use_case]  # <-- Añadir DI
):
    try:
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip()
        password = data.get('password') or ''

        # 1. Validar campos vacíos antes de cualquier otra validación
        if not email or not password:
            payload, status = build_auth_error(AuthErrorCode.EMPTY_FIELDS)
            return jsonify(payload), status

        # 2. Validar formato (correo válido, etc.) vía schema
        try:
            schema = LoginSchema(email=email, password=password)
        except ValidationError:
            payload, status = build_auth_error(AuthErrorCode.INVALID_EMAIL)
            return jsonify(payload), status

        # 3. Ejecutar caso de uso
        login_dto = LoginRequestDTO(
            email=schema.email,
            password=schema.password
        )
        result, error = login_use_case.execute(login_dto)

        if error:
            payload, status = build_auth_error(error)
            return jsonify(payload), status

        if isinstance(result, dict):
            return jsonify(result), 200
        elif hasattr(result, '__dict__'):
            return jsonify(result.__dict__), 200
        else:
            return jsonify({"result": str(result)}), 200

    except Exception as e:
        print(f"Login endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()
        payload, status = build_auth_error(AuthErrorCode.SERVER_ERROR)
        return jsonify(payload), status

@auth_bp.route('/register', methods=['POST'])
@inject
def register(
    register_use_case: RegisterUserUseCase = Provide[MainContainer.register_use_case]
):
    """Endpoint para registro de usuarios"""
    try:
        validated_data = RegisterSchema(**request.json)
        data_for_dto = validated_data.model_dump()
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    
    try:
        register_request = RegisterRequestDTO(**data_for_dto)
        result, error = register_use_case.execute(register_request)
        
        if error:
            return jsonify({"error": error}), 400
        
        if result is None:
            return jsonify({"error": "Registration failed - no result"}), 400
        
        if isinstance(result, str):
            current_app.logger.error(f"String result instead of DTO: {result}")
            return jsonify({"error": "Internal server error"}), 500
        
        try:
            if hasattr(result, 'model_dump'):
                return jsonify(result.model_dump()), 201
            elif hasattr(result, '__dict__'):
                return jsonify(result.__dict__), 201
            else:
                return jsonify({"success": True, "user_id": getattr(result, 'user_id', 'unknown')}), 201
        except Exception as e:
            current_app.logger.error(f"Error serializing result: {str(e)}")
            return jsonify({"error": "Registration successful but response serialization failed"}), 201
            
    except Exception as e:
        current_app.logger.error(f"Register endpoint error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
@inject
def forgot_password(
    forgot_password_use_case: ForgotPasswordUseCase = Provide[MainContainer.forgot_password_use_case]
):
    """Solicitar reseteo de contraseña"""
    try:

        validated_data = ForgotPasswordSchema(**request.json)
        data = validated_data.model_dump()

        request_dto = ForgotPasswordRequestDTO(email=data['email'])

        result = forgot_password_use_case.execute(request_dto)

        return jsonify({
            'success': result.success,
            'message': result.message,
            'user_id': result.user_id
        }), 200 if result.success else 400
        
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        current_app.logger.error(f"Forgot password error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@auth_bp.route('/reset-password', methods=['POST'])
@inject
def reset_password(
    reset_password_use_case: ResetPasswordUseCase = Provide[MainContainer.reset_password_use_case]
):
    """Confirmar reseteo de contraseña"""
    try:
        validated_data = ResetPasswordSchema(**request.json)
        data = validated_data.model_dump()

        request_dto = ResetPasswordConfirmDTO(
            token=data['token'],
            new_password=data['new_password']
        )
        
        result = reset_password_use_case.execute(request_dto)
        
        return jsonify({
            'success': result.success,
            'message': result.message,
            'user_id': result.user_id,
            'email': result.email
        }), 200 if result.success else 400
        
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        current_app.logger.error(f"Reset password error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': 'An error occurred while resetting your password'
        }), 500


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
            "/api/v1/auth/forgot-password",
            "/api/v1/auth/reset-password",
            "/api/v1/auth/refresh",
            "/api/v1/auth/logout",
            "/api/v1/auth/verify"
        ]
    })