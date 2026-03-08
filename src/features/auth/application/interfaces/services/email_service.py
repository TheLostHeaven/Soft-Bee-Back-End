# src/features/auth/application/interfaces/services/email_service.py
from abc import ABC, abstractmethod
from src.features.auth.domain.entities.user import User

class IEmailService(ABC):
    """Interface para servicio de envío de emails"""
    
    @abstractmethod
    def send_password_reset_email(self, user: User, reset_token: str) -> bool:
        """Envía un email de reseteo de contraseña"""
        pass
    
    # @abstractmethod
    # def send_welcome_email(self, user: User) -> bool:
    #     """Envía un email de bienvenida"""
    #     pass
    
    # @abstractmethod
    # def send_verification_email(self, user: User, verification_token: str) -> bool:
    #     """Envía un email de verificación"""
    #     pass