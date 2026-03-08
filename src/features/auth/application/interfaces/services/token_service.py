from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class ITokenService(ABC):
    """Interface/Port para servicio de tokens"""
    
    @abstractmethod
    def create_access_token(self, data: Dict[str, Any], expires_in: int = 900) -> str:
        """Crear access token JWT"""
        pass
    
    @abstractmethod
    def create_refresh_token(self, data: Dict[str, Any], expires_in: int = 2592000) -> str:
        """Crear refresh token JWT"""
        pass
    
    # @abstractmethod
    # def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
    #     """Verificar y decodificar token"""
    #     pass
    
    # @abstractmethod
    # def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
    #     """Decodificar token sin verificar"""
    #     pass
    
    # @abstractmethod
    # def is_token_expired(self, token: str) -> bool:
    #     """Verificar si token está expirado"""
    #     pass
    
    # @abstractmethod
    # def get_token_expiry(self, token: str) -> Optional[datetime]:
    #     """Obtener fecha de expiración del token"""
    #     pass

    # Alias para compatibilidad
    def generate_access_token(self, user_id: str, email: str) -> str:
        """Alias para create_access_token"""
        return self.create_access_token(user_id, email)
    
    def generate_refresh_token(self, user_id: str, email: str) -> str:
        """Alias para create_refresh_token"""
        return self.create_refresh_token(user_id, email)