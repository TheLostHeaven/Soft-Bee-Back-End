# src/features/auth/infrastructure/repositories/user_repository_impl.py

from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime  # <-- CAMBIÉ de 'import datetime' a 'from datetime import datetime'
import logging

from ...domain.entities.user import User
from ...domain.value_objects.email import Email
from ...application.interfaces.repositories.user_repository import IUserRepository
from ...application.mappers.user_mapper import UserMapper
from ..models.user_model import UserModel

logger = logging.getLogger(__name__)

class UserRepositoryImpl(IUserRepository):
    """Implementación del repositorio de usuarios con SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save(self, user: User) -> User:
        user_model = UserMapper.to_model(user)
        if user.id:
            existing = self.db_session.query(UserModel).filter_by(id=user.id).first()
            if existing:
                existing.email = user.email.value
                existing.username = user.username
                existing.hashed_password = user.hashed_password
                existing.first_name = user.first_name
                existing.last_name = user.last_name
                existing.phone = user.phone
                existing.is_active = user.is_active
                existing.is_verified = user.is_verified
                existing.last_login = user.last_login
                existing.refresh_tokens = user.refresh_tokens
                existing.failed_login_attempts = user.failed_login_attempts
                existing.updated_at = datetime.utcnow()
                user_model = existing
            else:
                self.db_session.add(user_model)
        else:
            self.db_session.add(user_model)
        
        self.db_session.flush()
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
        """
        Busca un usuario por email.
        
        Args:
            email: Puede ser string o objeto Email
            
        Returns:
            Optional[User]: Usuario encontrado o None
        """
        try:
            # Convertir a string si es un objeto Email
            email_str = email.value if hasattr(email, 'value') else email
            
            user_model = self.db_session.query(UserModel).filter_by(email=email_str).first()
            
            if user_model:
                # Mapper convierte UserModel a User con Email Value Object
                return UserMapper.to_entity(user_model)
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by email: {str(e)}")  # <-- CAMBIÉ self.logger a logger
            return None
    
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
        return result > 0
    
    def update_last_login(self, user_id):
        """Actualizar último login del usuario"""
        try:
            # Si user_id ya es UUID, no lo conviertas de nuevo
            if isinstance(user_id, UUID):
                user_uuid = user_id
            else:
                # Si es string, conviértelo a UUID
                try:
                    user_uuid = UUID(str(user_id))
                except ValueError as e:
                    logger.error(f"Invalid UUID format: {user_id}, error: {e}")
                    return False
            
            # CORRECCIÓN: Usar self.db_session en lugar de self.session
            user = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
            if user:
                user.last_login = datetime.utcnow()  # <-- Ahora datetime está importado correctamente
                self.db_session.commit()  # <-- CORRECCIÓN
                return True
            return False
            
        except Exception as e:
            self.db_session.rollback()  # <-- CORRECCIÓN
            logger.error(f"Error updating last login: {str(e)}")
            return False
    
    def add_refresh_token(self, user_id: str, token: str) -> None:
        """Añadir refresh token al usuario"""
        try:
            # Manejar tanto UUID como string
            if isinstance(user_id, UUID):
                user_uuid = user_id
            else:
                try:
                    user_uuid = UUID(str(user_id))
                except ValueError as e:
                    logger.error(f"Invalid UUID format: {user_id}, error: {e}")
                    return
            
            user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
            if user_model:
                if not user_model.refresh_tokens:
                    user_model.refresh_tokens = []
                
                if token not in user_model.refresh_tokens:
                    user_model.refresh_tokens.append(token)
                    self.db_session.commit()  # Añadir commit para guardar cambios
        
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error adding refresh token: {str(e)}")
    
    def remove_refresh_token(self, user_id: str, token: str) -> bool:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return False
        
        user_model = self.db_session.query(UserModel).filter_by(id=user_uuid).first()
        if user_model and user_model.refresh_tokens and token in user_model.refresh_tokens:
            user_model.refresh_tokens.remove(token)
            self.db_session.commit()  # Añadir commit
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
    
    def find_by_reset_token(self, reset_token: str) -> Optional[User]:
        """
        Busca un usuario por su token de reseteo de contraseña.
        
        Args:
            reset_token: Token de reseteo
            
        Returns:
            Optional[User]: Usuario encontrado o None
        """
        try:
            user_model = self.db_session.query(UserModel).filter_by(
                reset_token=reset_token
            ).first()
            
            if user_model:
                return UserMapper.to_entity(user_model)
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by reset token: {str(e)}")  # <-- CAMBIÉ
            return None