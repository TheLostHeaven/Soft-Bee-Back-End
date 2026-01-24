# src/features/auth/application/use_cases/forgot_password.py
import logging
from typing import Optional
from datetime import datetime, timedelta
from src.features.auth.application.dto.reset_password_dto import ForgotPasswordRequestDTO, PasswordResetResultDTO
from src.features.auth.application.interfaces.repositories.user_repository import IUserRepository
from src.features.auth.application.interfaces.services.email_service import IEmailService
from src.features.auth.application.interfaces.services.token_service import ITokenService

logger = logging.getLogger(__name__)

class ForgotPasswordUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        email_service: IEmailService,
        token_service: ITokenService
    ):
        self.user_repository = user_repository
        self.email_service = email_service
        self.token_service = token_service
    
    def execute(self, request_dto: ForgotPasswordRequestDTO) -> PasswordResetResultDTO:
        try:
            logger.info(f"Processing forgot password request for email: {request_dto.email}")
            
            # Buscar usuario por email
            user = self.user_repository.find_by_email(request_dto.email)
            
            if not user:
                # Por seguridad, no revelamos si el usuario existe
                logger.info(f"No user found for email: {request_dto.email}, but returning success for security")
                return PasswordResetResultDTO(
                    success=True,
                    message="If your email is registered, you will receive a password reset link shortly.",
                    user_id=None
                )
            
            # Verificar si el usuario está activo
            if not user.is_active:
                logger.warning(f"User {user.email} is not active, cannot reset password")
                return PasswordResetResultDTO(
                    success=False,
                    message="Your account is not active. Please contact support.",
                    user_id=user.id
                )
            
            # Generar token de reset
            reset_token = self.token_service.generate_reset_token()
            
            # Establecer token en el usuario
            user.set_reset_token(reset_token, expires_in_minutes=30)
            
            # Guardar usuario con token
            self.user_repository.save(user)
            
            # Enviar email
            self.email_service.send_password_reset_email(user, reset_token)
            
            logger.info(f"Password reset email sent to {user.email}")
            
            return PasswordResetResultDTO(
                success=True,
                message="If your email is registered, you will receive a password reset link shortly.",
                user_id=user.id
            )
            
        except Exception as e:
            logger.error(f"Error in ForgotPasswordUseCase: {str(e)}")
            raise