# src/features/auth/application/use_cases/login_user.py
import logging
from uuid import UUID
from src.features.auth.application.dto.auth_dto import LoginRequestDTO
from ...application.interfaces.repositories.user_repository import IUserRepository
from ...application.interfaces.services.token_service import ITokenService
from src.features.auth.application.interfaces.services.password_service import IPasswordService

logger = logging.getLogger(__name__)

class LoginUserUseCase:
    """Caso de uso: Login de usuario"""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
        password_service: IPasswordService
    ):
        self.user_repository = user_repository
        self.token_service = token_service
        self.password_service = password_service
    
    def execute(self, request_dto: LoginRequestDTO):
        try:
            logger.info(f"Attempting login for email: {request_dto.email}")
            
            # 1. Buscar usuario
            user = self.user_repository.find_by_email(request_dto.email)
            
            if not user:
                logger.warning(f"User not found: {request_dto.email}")
                return None, "Invalid email or password"
            
            # 2. Verificar si está activo
            if not user.is_active:
                logger.warning(f"User not active: {request_dto.email}")
                return None, "Account is not active"
            
            # 3. Verificar contraseña
            password_valid = self.password_service.verify_password(
                request_dto.password,
                user.hashed_password
            )
            
            if not password_valid:
                logger.warning(f"Invalid password for: {request_dto.email}")
                return None, "Invalid email or password"
            
            # 4. Actualizar último login - Pasar el user.id directamente (ya es UUID)
            self.user_repository.update_last_login(user.id)
            
            # 5. Preparar datos para tokens
            user_id_str = str(user.id)
            email_str = user.email.value if hasattr(user.email, 'value') else str(user.email)
            
            # 6. Generar tokens
            # Usar generate_access_token si existe
            if hasattr(self.token_service, 'generate_access_token'):
                access_token = self.token_service.generate_access_token(
                    user_id=user_id_str,
                    email=email_str
                )
                refresh_token = self.token_service.generate_refresh_token(
                    user_id=user_id_str,
                    email=email_str
                )
            # Si no, usar create_access_token
            elif hasattr(self.token_service, 'create_access_token'):
                token_data = {
                    "sub": user_id_str,
                    "email": email_str,
                    "user_id": user_id_str
                }
                access_token = self.token_service.create_access_token(token_data)
                refresh_token = self.token_service.create_refresh_token(token_data)
            else:
                # Método alternativo
                access_token = self.token_service.create_access_token(
                    subject=user_id_str,
                    email=email_str
                )
                refresh_token = self.token_service.create_refresh_token(
                    subject=user_id_str,
                    email=email_str
                )
            
            # 7. Añadir refresh token al usuario
            self.user_repository.add_refresh_token(user.id, refresh_token)
            
            logger.info(f"Login successful for: {request_dto.email}")
            
            # 8. Crear respuesta
            response = {
                "user_id": user_id_str,
                "email": email_str,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 3600
            }
            
            # Si necesitas username en la respuesta
            if hasattr(user, 'username') and user.username:
                response["username"] = user.username
            
            return response, None
            
        except Exception as e:
            logger.error(f"Error in LoginUserUseCase: {str(e)}", exc_info=True)
            import traceback
            traceback.print_exc()
            return None, "Internal server error"