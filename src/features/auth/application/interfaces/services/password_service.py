# src/features/auth/application/interfaces/services/password_service.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IPasswordService(ABC):
    """Interface para servicio de manejo de contraseñas"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hashea una contraseña"""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica una contraseña"""
        pass
    
    # Estos métodos son opcionales si no los usas:
    # @abstractmethod
    # def generate_jwt_token(self, payload: Dict[str, Any], expires_minutes: int = 30) -> str:
    #     pass
    
    # @abstractmethod
    # def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
    #     pass  