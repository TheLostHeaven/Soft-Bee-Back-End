from typing import Tuple, Optional, Dict, Any
from datetime import datetime
from ...domain.entities.user import User
from ...domain.value_objects.email import Email
from ...application.dto.auth_dto import RegisterRequestDTO, RegisterResponseDTO
from ...application.interfaces.repositories.user_repository import IUserRepository
from ...domain.exceptions.auth_exceptions import EmailAlreadyExistsException

class RegisterUserUseCase:
    """Caso de uso: Registrar usuario"""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: Any,
        event_publisher: Optional[Any] = None
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.event_publisher = event_publisher
    
    def execute(self, request: RegisterRequestDTO) -> Tuple[Optional[RegisterResponseDTO], Optional[str]]:
        """
        Ejecutar registro de usuario
        
        Returns:
            Tuple[Optional[RegisterResponseDTO], Optional[str]]: (response, error_message)
        """
        try:
            # 1. Verificar si email ya existe
            if self.user_repository.exists_by_email(request.email):
                raise EmailAlreadyExistsException()
            
            # 2. Verificar si username ya existe
            if self.user_repository.exists_by_username(request.username):
                return None, "Username already exists"
            
            # 3. Hash password
            hashed_password_tuple = self.password_hasher.hash(request.password)
            hashed_password_string = hashed_password_tuple[0]
            
            # 4. Crear entidad de dominio
            user = User(
                email=Email(request.email),
                username=request.username,
                hashed_password=hashed_password_string,
                phone=request.phone
            )
            
            # 5. Guardar usuario
            saved_user = self.user_repository.save(user)
            
            # 6. Publicar evento si hay publisher
            if self.event_publisher:
                events = saved_user.pull_events()
                for event in events:
                    self.event_publisher.publish(event)
            
            # 7. Crear respuesta
            response = RegisterResponseDTO(
                id=saved_user.id,
                email=str(saved_user.email),
                username=saved_user.username,
                is_verified=saved_user.is_verified,
                created_at=saved_user.created_at
            )
            
            return response, None
            
        except Exception as e:
            return None, str(e)