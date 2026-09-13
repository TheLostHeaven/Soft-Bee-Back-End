# src/features/auth/application/use_cases/refresh_token.py
import logging

from src.features.auth.application.dto.auth_dto import (
    RefreshTokenRequestDTO,
    RefreshTokenResponseDTO,
)
from src.features.auth.application.errors import AuthErrorCode
from ...application.interfaces.repositories.user_repository import IUserRepository
from ...application.interfaces.services.token_service import ITokenService

logger = logging.getLogger(__name__)

# Duración del access token (segundos). Debe coincidir con el valor por defecto
# usado al generar los tokens (1 hora).
ACCESS_TOKEN_EXPIRES_IN = 3600


class RefreshTokenUseCase:
    """Caso de uso: refrescar el access token a partir de un refresh token válido.

    Aplica rotación de refresh token: el refresh token usado se invalida y se
    emite uno nuevo, evitando la reutilización de tokens antiguos.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
    ):
        self.user_repository = user_repository
        self.token_service = token_service

    def execute(self, request_dto: RefreshTokenRequestDTO):
        try:
            refresh_token = (request_dto.refresh_token or "").strip()

            if not refresh_token:
                return None, AuthErrorCode.INVALID_TOKEN

            # 1. Decodificar y validar firma/expiración del refresh token
            try:
                payload = self.token_service.decode_token(refresh_token)
            except ValueError as e:
                logger.warning(f"Refresh token inválido o expirado: {str(e)}")
                return None, AuthErrorCode.INVALID_TOKEN

            # 2. Verificar que sea del tipo correcto
            if payload.get("type") != "refresh":
                logger.warning("Se recibió un token que no es de tipo refresh")
                return None, AuthErrorCode.INVALID_TOKEN

            user_id = payload.get("user_id") or payload.get("sub")
            email = payload.get("email")

            if not user_id:
                logger.warning("Refresh token sin identificador de usuario")
                return None, AuthErrorCode.INVALID_TOKEN

            # 3. Verificar que el refresh token siga vigente para el usuario
            #    (no revocado por logout o rotación previa)
            if not self.user_repository.has_refresh_token(str(user_id), refresh_token):
                logger.warning(f"Refresh token no reconocido para el usuario {user_id}")
                return None, AuthErrorCode.INVALID_TOKEN

            # 4. Verificar que el usuario siga existiendo y esté activo
            user = self.user_repository.find_by_id(str(user_id))
            if not user:
                logger.warning(f"Usuario no encontrado al refrescar token: {user_id}")
                return None, AuthErrorCode.INVALID_TOKEN

            if not user.is_active:
                logger.warning(f"Usuario inactivo al refrescar token: {user_id}")
                return None, AuthErrorCode.ACCOUNT_DISABLED

            email_str = email or (
                user.email.value if hasattr(user.email, "value") else str(user.email)
            )

            # 5. Generar nuevo access token
            new_access_token = self.token_service.generate_access_token(
                user_id=str(user_id),
                email=email_str,
                expires_in=ACCESS_TOKEN_EXPIRES_IN,
            )

            # 6. Rotación de refresh token: invalidar el anterior y emitir uno nuevo
            new_refresh_token = self.token_service.generate_refresh_token(
                user_id=str(user_id),
                email=email_str,
            )
            self.user_repository.remove_refresh_token(str(user_id), refresh_token)
            self.user_repository.add_refresh_token(str(user_id), new_refresh_token)

            logger.info(f"Access token refrescado para el usuario {user_id}")

            response = RefreshTokenResponseDTO(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRES_IN,
            )

            return response, None

        except Exception as e:
            logger.error(f"Error in RefreshTokenUseCase: {str(e)}", exc_info=True)
            return None, AuthErrorCode.SERVER_ERROR
