# src/features/auth/application/use_cases/register_user.py
import logging
from src.features.auth.application.dto.auth_dto import RegisterRequestDTO, RegisterResponseDTO
from src.features.auth.application.interfaces.repositories.user_repository import IUserRepository
from src.features.auth.application.interfaces.services.token_service import ITokenService
from src.features.auth.application.interfaces.services.password_service import IPasswordService

from src.features.auth.domain.entities.user import User
from src.features.auth.domain.value_objects.email import Email

logger = logging.getLogger(__name__)

class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService,
        token_service: ITokenService
    ):
        self.user_repository = user_repository
        self.token_service = token_service
        self.password_service = password_service
    
    # **CORRECCIÓN: ESTE MÉTODO DEBE ESTAR INDENTADO DENTRO DE LA CLASE**
    def execute(self, request_dto: RegisterRequestDTO):
        """
        Ejecuta el registro de un nuevo usuario
        
        Returns:
            tuple: (RegisterResponseDTO, error_message) o (None, error_message)
        """
        try:
            logger.info(f"Attempting registration for email: {request_dto.email}")
            
            # 1. Verificar si el usuario ya existe por email
            existing_user = self.user_repository.find_by_email(request_dto.email)
            if existing_user:
                logger.warning(f"Registration failed: email already exists {request_dto.email}")
                return None, "Email already registered"
            
            # 2. Verificar si el username ya existe
            existing_user_by_username = self.user_repository.find_by_username(request_dto.username)
            if existing_user_by_username:
                logger.warning(f"Registration failed: username already exists {request_dto.username}")
                return None, "Username already taken"
            
            # 3. Hashear la contraseña
            hashed_password = self.password_service.hash_password(request_dto.password)
            
            # 4. Crear Email Value Object
            email_obj = Email(request_dto.email)
            
            # 5. Crear entidad de usuario
            user = User(
                email=email_obj,
                username=request_dto.username,
                hashed_password=hashed_password,
                phone=request_dto.phone,
                is_active=True,
                is_verified=False
            )
            
            # 6. Guardar usuario en la base de datos
            saved_user = self.user_repository.save(user)
            
            # 7. Generar tokens de autenticación
            
            access_token = self.token_service.generate_access_token(
                user_id=str(saved_user.id),
                email=saved_user.email.value,
                expires_in=3600
            )
            
            refresh_token = self.token_service.generate_refresh_token(
                user_id=str(saved_user.id),
                email=saved_user.email.value,
                expires_in=2592000
            )
            
            # 8. Añadir refresh token al usuario
            self.user_repository.add_refresh_token(str(saved_user.id), refresh_token)
            
            logger.info(f"Registration successful for user: {saved_user.email}")
            
            # 9. Crear y retornar respuesta DTO
            response = RegisterResponseDTO(
                user_id=str(saved_user.id),
                email=saved_user.email.value,
                username=saved_user.username,
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=3600
            )
            
            return response, None
            
        except Exception as e:
            logger.error(f"Error in RegisterUserUseCase: {str(e)}", exc_info=True)
            return None, str(e)