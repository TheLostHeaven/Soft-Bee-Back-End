from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from ...domain.entities.user import User
from ...domain.value_objects.email import Email
from ...application.interfaces.repositories.user_repository import IUserRepository
from ...application.mappers.user_mapper import UserMapper
from ..models.user_model import UserModel
import datetime

class UserRepositoryImpl(IUserRepository):
    """Implementación del repositorio de usuarios con SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, user: User) -> User:
        user_model = UserMapper.to_model(user)
        # Check if user already exists (for update scenarios)
        if user.id:
            existing = self.db_session.query(UserModel).filter_by(id=user.id).first()
            if existing:
                # Manually update existing user attributes from the user entity
                existing.email = user.email.value
                existing.username = user.username
                existing.hashed_password = user.hashed_password
                existing.phone = user.phone
                existing.is_active = user.is_active
                existing.is_verified = user.is_verified
                existing.last_login = user.last_login
                existing.refresh_tokens = user.refresh_tokens
                existing.failed_login_attempts = user.failed_login_attempts
                existing.updated_at = datetime.datetime.utcnow() # Update updated_at
                user_model = existing # Set user_model to existing for refresh
            else:
                self.db_session.add(user_model)
        else:
            self.db_session.add(user_model)
        self.db_session.flush() # Use flush to ensure ID is generated if new, but don't commit yet
        self.db_session.refresh(user_model) # Refresh to get the generated ID
        return UserMapper.to_entity(user_model)
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        return UserMapper.to_entity(user_model) if user_model else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_model = self.db_session.query(UserModel).filter_by(email=email).first()
        return UserMapper.to_entity(user_model) if user_model else None
    
    def find_by_username(self, username: str) -> Optional[User]:
        user_model = self.db_session.query(UserModel).filter_by(username=username).first()
        return UserMapper.to_entity(user_model) if user_model else None
    
    def exists_by_email(self, email: str) -> bool:
        return self.db_session.query(
            self.db_session.query(UserModel).filter_by(email=email).exists()
        ).scalar()
    
    def exists_by_username(self, username: str) -> bool:
        return self.db_session.query(
            self.db_session.query(UserModel).filter_by(username=username).exists()
        ).scalar()
    
    def delete(self, user_id: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False
        
        result = self.db_session.query(UserModel).filter_by(id=user_uuid).delete()
        # self.db_session.commit() # Removed explicit commit
        self.db_session.flush() # Flush to ensure delete operation takes effect within the session
        return result > 0
    
    def update_last_login(self, user_id: str) -> None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        if user_model:
            user_model.last_login = datetime.datetime.utcnow()
            # self.db_session.commit() # Removed explicit commit
            self.db_session.flush() # Flush to ensure update operation takes effect within the session
    
    def add_refresh_token(self, user_id: str, token: str) -> None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        if user_model:
            if not user_model.refresh_tokens:
                user_model.refresh_tokens = []
            
            if token not in user_model.refresh_tokens:
                user_model.refresh_tokens.append(token)
                # self.db_session.commit() # Removed explicit commit
                self.db_session.flush() # Flush to ensure update operation takes effect within the session
    
    def remove_refresh_token(self, user_id: str, token: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        if user_model and user_model.refresh_tokens and token in user_model.refresh_tokens:
            user_model.refresh_tokens.remove(token)
            # self.db_session.commit() # Removed explicit commit
            self.db_session.flush() # Flush to ensure update operation takes effect within the session
            return True
        
        return False
    
    def has_refresh_token(self, user_id: str, token: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        return bool(
            user_model and 
            user_model.refresh_tokens and 
            token in user_model.refresh_tokens
        )