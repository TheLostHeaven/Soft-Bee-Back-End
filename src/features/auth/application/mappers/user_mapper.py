# src/features/auth/application/mappers/user_mapper.py
import logging
from src.features.auth.domain.entities.user import User
from src.features.auth.domain.value_objects.email import Email  # <-- Importar Email
from src.features.auth.infrastructure.models.user_model import UserModel

logger = logging.getLogger(__name__)

class UserMapper:
    @staticmethod
    def to_entity(user_model: UserModel) -> User:
        """
        Convierte un UserModel a una entidad User con Email Value Object
        """
        try:
            if not user_model:
                return None
            
            # **CREAR EMAIL VALUE OBJECT A PARTIR DEL STRING EN LA BD**
            email_obj = Email(user_model.email)
            
            user = User(
                id=user_model.id,  # Ya debería ser UUID
                email=email_obj,   # <-- Email Value Object
                username=user_model.username,
                hashed_password=user_model.hashed_password,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                phone=user_model.phone,
                is_active=user_model.is_active,
                is_verified=user_model.is_verified,
                reset_token=user_model.reset_token,
                reset_token_expiry=user_model.reset_token_expiry,
                last_login=user_model.last_login,
                refresh_tokens=user_model.refresh_tokens or [],
                failed_login_attempts=user_model.failed_login_attempts or 0,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at
            )
            
            return user
            
        except Exception as e:
            logger.error(f"Error mapping UserModel to User entity: {str(e)}")
            raise
    
    @staticmethod
    def to_model(user: User) -> UserModel:
        """
        Convierte una entidad User a UserModel
        """
        try:
            # **OBTENER STRING DEL EMAIL VALUE OBJECT**
            email_str = user.email.value if hasattr(user.email, 'value') else str(user.email)
            
            user_model = UserModel(
                id=str(user.id) if user.id else None,
                email=email_str,  # <-- Guardar como string
                username=user.username,
                hashed_password=user.hashed_password,
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                is_active=user.is_active,
                is_verified=user.is_verified,
                reset_token=user.reset_token,
                reset_token_expiry=user.reset_token_expiry,
                last_login=user.last_login,
                refresh_tokens=user.refresh_tokens,
                failed_login_attempts=user.failed_login_attempts,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
            return user_model
            
        except Exception as e:
            logger.error(f"Error mapping User entity to UserModel: {str(e)}")
            raise