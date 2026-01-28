from abc import ABC, abstractmethod
from typing import Optional
from src.features.auth.domain.entities.user import User
from uuid import UUID

class IUserRepository(ABC):
    """Interface/Port para repositorio de usuarios"""

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Buscar usuario por ID"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualizar usuario"""
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        """Eliminar usuario"""
        pass
