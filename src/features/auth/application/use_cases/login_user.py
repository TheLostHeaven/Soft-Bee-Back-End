from typing import Tuple, Optional, Dict, Any
from datetime import datetime, timedelta
from ...application.dto.auth_dto import LoginRequestDTO, LoginResponseDTO
from ...application.interfaces.repositories.user_repository import IUserRepository
from ...application.interfaces.services.token_service import ITokenService
from ...domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    AccountLockedException,
    UserNotFoundException
)

class LoginUserUseCase:
    """Caso de uso: Login de usuario"""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
        password_hasher: Any  # PasswordHasher implementación
    ):
        self.user_repository = user_repository
        self.token_service = token_service
        self.password_hasher = password_hasher
    
    def execute(self, request: LoginRequestDTO) -> Tuple[Optional[LoginResponseDTO], Optional[str]]:
        """
        Ejecutar login de usuario
        
        Returns:
            Tuple[Optional[LoginResponseDTO], Optional[str]]: (response, error_message)
        """
        try:
            # 1. Buscar usuario por email
            user = self.user_repository.find_by_email(request.email)
            if not user:
                raise UserNotFoundException()
            
            # 2. Verificar si la cuenta está bloqueada
            if user.is_locked():
                raise AccountLockedException()
            
            # 3. Verificar password
            if not self.password_hasher.verify(request.password, user.hashed_password):
                user.login_failed()
                self.user_repository.save(user)
                raise InvalidCredentialsException()
            
            # 4. Login exitoso
            user.login_successful()
            self.user_repository.save(user)
            
            # 5. Generar tokens
            token_data = {
                "sub": user.id,
                "email": str(user.email),
                "username": user.username,
                "is_verified": user.is_verified
            }
            
            access_token = self.token_service.create_access_token(
                token_data,
                expires_in=86400 if request.remember_me else 900  # 24h o 15min
            )
            
            refresh_token = self.token_service.create_refresh_token(
                {"sub": user.id},
                expires_in=2592000 if request.remember_me else 604800  # 30d o 7d
            )
            
            # 6. Guardar refresh token
            self.user_repository.add_refresh_token(user.id, refresh_token)
            
            # 7. Crear respuesta
            response = LoginResponseDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=86400 if request.remember_me else 900,
                user={
                    "id": user.id,
                    "email": str(user.email),
                    "username": user.username,
                    "is_verified": user.is_verified,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
            )
            
            return response, None
            
        except Exception as e:
            # Manejar excepciones específicas
            error_message = str(e)
            if isinstance(e, (InvalidCredentialsException, UserNotFoundException)):
                error_message = "Invalid email or password"
            elif isinstance(e, AccountLockedException):
                error_message = "Account is locked due to multiple failed attempts"
            
            return None, error_message