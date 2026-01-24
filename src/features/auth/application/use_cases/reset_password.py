# src/features/auth/application/use_cases/reset_password_use_case.py
import logging
from datetime import datetime
from typing import Optional
# from src.features.auth.application.dto.reset_password_dto import  ResetPasswordConfirmDTO, ResetPasswordResultDTO
from src.features.auth.application.dto.reset_password_dto import ResetPasswordConfirmDTO, PasswordResetResultDTO
from src.features.auth.application.interfaces.repositories.user_repository import IUserRepository
from src.features.auth.application.interfaces.services.password_service import IPasswordService
from src.features.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
    InvalidResetTokenException,
    PasswordResetException
)

logger = logging.getLogger(__name__)

class ResetPasswordUseCase:
    """
    Caso de uso para resetear la contraseña de un usuario.
    
    Responsabilidades:
    1. Validar el token de reseteo
    2. Verificar que el token no haya expirado
    3. Hashear la nueva contraseña
    4. Actualizar la contraseña del usuario
    5. Limpiar el token de reseteo
    """
    
    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService
    ):
        """
        Args:
            user_repository: Repositorio de usuarios para operaciones de BD
            password_service: Servicio para hashear y verificar contraseñas
        """
        self.user_repository = user_repository
        self.password_service = password_service
    
    def execute(self, request_dto: ResetPasswordConfirmDTO) -> PasswordResetResultDTO:
        """
        Ejecuta el proceso de reseteo de contraseña.
        
        Args:
            request_dto: DTO con token y nueva contraseña
            
        Returns:
            ResetPasswordResultDTO: Resultado de la operación
            
        Raises:
            InvalidResetTokenException: Si el token es inválido o ha expirado
            UserNotFoundException: Si el usuario no existe
            PasswordResetException: Si hay un error en el proceso
        """
        try:
            logger.info(f"Processing password reset request with token: {request_dto.token[:8]}...")
            
            # 1. Buscar usuario por token de reseteo
            user = self.user_repository.find_by_reset_token(request_dto.token)
            
            if not user:
                logger.warning(f"Invalid reset token: {request_dto.token[:8]}...")
                raise InvalidResetTokenException("Invalid or expired reset token")
            
            # 2. Verificar que el token sea válido (no haya expirado)
            if not self._is_reset_token_valid(user):
                logger.warning(f"Expired reset token for user: {user.email}")
                # Limpiar token expirado
                user.reset_token = None
                user.reset_token_expiry = None
                self.user_repository.save(user)
                
                raise InvalidResetTokenException("Reset token has expired")
            
            # 3. Verificar que el usuario esté activo
            if not user.is_active:
                logger.warning(f"User {user.email} is not active, cannot reset password")
                raise PasswordResetException("User account is not active")
            
            # 4. Validar fortaleza de la nueva contraseña
            self._validate_password_strength(request_dto.new_password)
            
            # 5. Hashear la nueva contraseña
            new_password_hash = self.password_service.hash_password(request_dto.new_password)
            
            # 6. Actualizar la contraseña del usuario
            user.hashed_password = new_password_hash
            
            # 7. Limpiar el token de reseteo (ya fue usado)
            user.reset_token = None
            user.reset_token_expiry = None
            
            # 8. Guardar cambios
            self.user_repository.save(user)
            
            logger.info(f"Password successfully reset for user: {user.email}")
            
            return PasswordResetResultDTO(
                success=True,
                message="Password has been reset successfully",
                user_id=user.id,
                email=user.email
            )
            
        except (InvalidResetTokenException, UserNotFoundException, PasswordResetException) as e:
            # Re-lanzar excepciones específicas del dominio
            raise
        except Exception as e:
            logger.error(f"Unexpected error in ResetPasswordUseCase: {str(e)}")
            raise PasswordResetException(f"Error resetting password: {str(e)}")
    
    def _is_reset_token_valid(self, user) -> bool:
        """
        Verifica si el token de reseteo es válido.
        
        Args:
            user: Entidad User con reset_token y reset_token_expiry
            
        Returns:
            bool: True si el token es válido, False si ha expirado
        """
        if not user.reset_token or not user.reset_token_expiry:
            return False
        
        current_time = datetime.utcnow()
        return current_time < user.reset_token_expiry
    
    def _validate_password_strength(self, password: str) -> None:
        """
        Valida la fortaleza de la nueva contraseña.
        
        Args:
            password: Contraseña a validar
            
        Raises:
            PasswordResetException: Si la contraseña no cumple los requisitos
        """
        if len(password) < 8:
            raise PasswordResetException("Password must be at least 8 characters long")
        
        if len(password) > 100:
            raise PasswordResetException("Password must be at most 100 characters long")
        
        # Opcional: agregar más validaciones de fortaleza
        # if not any(char.isdigit() for char in password):
        #     raise PasswordResetException("Password must contain at least one digit")
        # if not any(char.isupper() for char in password):
        #     raise PasswordResetException("Password must contain at least one uppercase letter")
        # if not any(char.islower() for char in password):
        #     raise PasswordResetException("Password must contain at least one lowercase letter")