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
        
        if user.id:
            # Actualizar usuario existente
            existing = self.db_session.query(UserModel).filter_by(id=user.id).first()
            if existing:
                for key, value in user_model.__dict__.items():
                    if not key.startswith('_'):
                        setattr(existing, key, value)
                user_model = existing
            else:
                self.db_session.add(user_model)
        else:
            # Crear nuevo usuario
            self.db_session.add(user_model)
        
        self.db_session.commit()
        self.db_session.refresh(user_model)
        
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
        self.db_session.commit()
        return result > 0
    
    def update_last_login(self, user_id: str) -> None:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        if user_model:
            user_model.last_login = datetime.utcnow()
            self.db_session.commit()
    
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
                self.db_session.commit()
    
    def remove_refresh_token(self, user_id: str, token: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        if user_model and user_model.refresh_tokens and token in user_model.refresh_tokens:
            user_model.refresh_tokens.remove(token)
            self.db_session.commit()
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