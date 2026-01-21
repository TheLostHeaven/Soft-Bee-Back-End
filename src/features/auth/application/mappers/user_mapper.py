from ...domain.entities.user import User
from ...infrastructure.models.user_model import UserModel
from ...domain.value_objects.email import Email
from ...domain.value_objects.password import Password
from uuid import UUID

class UserMapper:
    """Mapea entre la entidad User y el modelo UserModel"""

    @staticmethod
    def to_entity(user_model: UserModel) -> User:
        """Convierte un UserModel a una entidad User"""
        if not user_model:
            return None
        
        return User(
            id=str(user_model.id),
            email=Email(user_model.email),
            username=user_model.username,
            hashed_password=user_model.hashed_password,
            phone=user_model.phone,
            is_active=user_model.is_active,
            is_verified=user_model.is_verified,
            last_login=user_model.last_login,
            refresh_tokens=user_model.refresh_tokens or [],
            failed_login_attempts=user_model.failed_login_attempts,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )

    @staticmethod
    def to_model(user_entity: User) -> UserModel:
        """Convierte una entidad User a un UserModel"""
        if not user_entity:
            return None
            
        return UserModel(
            id=UUID(user_entity.id) if isinstance(user_entity.id, str) else user_entity.id,
            email=str(user_entity.email),
            username=user_entity.username,
            hashed_password=str(user_entity.hashed_password),
            phone=user_entity.phone,
            is_active=user_entity.is_active,
            is_verified=user_entity.is_verified,
            last_login=user_entity.last_login,
            refresh_tokens=user_entity.refresh_tokens,
            failed_login_attempts=user_entity.failed_login_attempts,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )
