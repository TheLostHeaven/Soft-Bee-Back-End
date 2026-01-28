import logging
from src.features.auth.domain.entities.user import User
from src.features.auth.domain.value_objects.email import Email
from src.features.auth.infrastructure.models.user_model import UserModel
from src.features.user.application.dto.user_dto import UserDTO, UpdateUserDTO
from uuid import UUID

logger = logging.getLogger(__name__)

class UserMapper:
    """Maps between User entity, UserModel, and UserDto"""

    @staticmethod
    def to_entity(user_model: UserModel) -> User:
        """
        Convierte un UserModel a una entidad User con Email Value Object
        """
        try:
            if not user_model:
                return None
            
            email_obj = Email(user_model.email)
            
            user = User(
                id=user_model.id,
                email=email_obj,
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
            email_str = user.email.value if hasattr(user.email, 'value') else str(user.email)
            
            user_model = UserModel(
                id=user.id if user.id else None,
                email=email_str,
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

    @staticmethod
    def to_dto(user_entity: User) -> UserDTO:
        """Converts a User entity to a UserDto"""
        if not user_entity:
            return None
        
        return UserDTO(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email.value,
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            phone=user_entity.phone,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )

    @staticmethod
    def from_update_dto_to_entity(update_dto: UpdateUserDTO, existing_entity: User) -> User:
        """Updates an existing User entity with data from UpdateUserDTO"""
        if not existing_entity:
            raise ValueError("Existing User entity cannot be None for update.")
        
        logger.info(f"UserMapper: Before update - existing_entity (username={existing_entity.username}, email={existing_entity.email.value}, phone={existing_entity.phone})")
        logger.info(f"UserMapper: Update DTO received - update_dto (username={update_dto.username}, email={update_dto.email}, phone={update_dto.phone})")
            
        existing_entity.username = update_dto.username if update_dto.username is not None else existing_entity.username
        existing_entity.email = Email(update_dto.email) if update_dto.email is not None else existing_entity.email
        existing_entity.first_name = update_dto.first_name if update_dto.first_name is not None else existing_entity.first_name
        existing_entity.last_name = update_dto.last_name if update_dto.last_name is not None else existing_entity.last_name
        existing_entity.phone = update_dto.phone if update_dto.phone is not None else existing_entity.phone
        
        logger.info(f"UserMapper: After update - existing_entity (username={existing_entity.username}, email={existing_entity.email.value}, phone={existing_entity.phone})")
        return existing_entity
