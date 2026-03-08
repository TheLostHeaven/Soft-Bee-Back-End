from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from src.features.auth.domain.entities.user import User
from src.features.user.application.interfaces.repositories.user_repository_interface import IUserRepository
from src.features.user.application.mappers.user_mapper import UserMapper
from src.features.auth.infrastructure.models.user_model import UserModel

logger = logging.getLogger(__name__)

class UserRepositoryImpl(IUserRepository):
    """Implementación del repositorio de usuarios con SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        logger.info(f"UserRepositoryImpl: Fetching user with ID {user_id}")
        user_model = self.db_session.query(UserModel).filter_by(id=user_id).first()
        if user_model:
            logger.info(f"UserRepositoryImpl: Found user_model for ID {user_id} (username: {user_model.username})")
        else:
            logger.info(f"UserRepositoryImpl: No user_model found for ID {user_id}")
        return UserMapper.to_entity(user_model) if user_model else None

    def update(self, user: User) -> User:
        logger.info(f"UserRepositoryImpl: Updating user with ID {user.id}")
        user_model = self.db_session.query(UserModel).filter_by(id=user.id).first()
        if user_model:
            logger.info(f"UserRepositoryImpl: Before update - user_model (username={user_model.username}, email={user_model.email}, phone={user_model.phone})")
            logger.info(f"UserRepositoryImpl: User entity values - user (username={user.username}, email={user.email.value}, phone={user.phone})")

            user_model.username = user.username
            user_model.email = user.email.value
            user_model.first_name = user.first_name
            user_model.last_name = user.last_name
            user_model.phone = user.phone
            user_model.updated_at = datetime.utcnow()
            
            logger.info(f"UserRepositoryImpl: After assignment - user_model (username={user_model.username}, email={user_model.email}, phone={user_model.phone})")

            try:
                self.db_session.flush() # Flush pending changes to the database
                self.db_session.commit()
                self.db_session.refresh(user_model) # Refresh the model to reflect committed changes
                logger.info(f"UserRepositoryImpl: User {user.id} updated and committed successfully.")
            except SQLAlchemyError as e:
                self.db_session.rollback()
                logger.error(f"UserRepositoryImpl: Error committing update for user {user.id}: {e}", exc_info=True)
                raise
            except Exception as e:
                self.db_session.rollback()
                logger.error(f"UserRepositoryImpl: Unexpected error during update for user {user.id}: {e}", exc_info=True)
                raise
        else:
            logger.warning(f"UserRepositoryImpl: No user_model found to update for ID {user.id}. This should not happen if existing_user was found in use case.")
        return UserMapper.to_entity(user_model)

    def delete(self, user_id: UUID) -> bool:
        logger.info(f"UserRepositoryImpl: Deleting user with ID {user_id}")
        try:
            result = self.db_session.query(UserModel).filter_by(id=user_id).delete()
            self.db_session.commit()
            if result > 0:
                logger.info(f"UserRepositoryImpl: User {user_id} deleted successfully.")
                return True
            else:
                logger.warning(f"UserRepositoryImpl: No user found with ID {user_id} to delete.")
                return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"UserRepositoryImpl: Error committing delete for user {user_id}: {e}", exc_info=True)
            raise
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"UserRepositoryImpl: Unexpected error during delete for user {user_id}: {e}", exc_info=True)
            raise
