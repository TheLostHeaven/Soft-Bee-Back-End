from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID  # Import UUID
from ...domain.value_objects.email import Email
from ...domain.value_objects.password import Password
from ...domain.events.auth_events import UserRegisteredEvent, UserLoggedInEvent
from ...domain.exceptions.auth_exceptions import InvalidUserException

@dataclass
class User:
    """Entidad User para autenticación"""
    
    email: Email
    username: str
    hashed_password: str
    id: Optional[UUID] = None  # Changed type from str to UUID
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    last_login: Optional[datetime] = None
    refresh_tokens: List[str] = field(default_factory=list)
    failed_login_attempts: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Eventos pendientes de publicación
    _events: List = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Validar reglas de negocio"""
        if len(self.username) < 3:
            raise InvalidUserException("Username must be at least 3 characters")
        
        if not self.email.is_valid():
            raise InvalidUserException("Invalid email address")
    
    def login_successful(self):
        """Manejar login exitoso"""
        self.last_login = datetime.utcnow()
        self.failed_login_attempts = 0
        self.updated_at = datetime.utcnow()
        
        # Registrar evento
        self._register_event(UserLoggedInEvent(
            user_id=self.id,
            email=str(self.email),
            timestamp=datetime.utcnow()
        ))
    
    def login_failed(self):
        """Manejar intento de login fallido"""
        self.failed_login_attempts += 1
        self.updated_at = datetime.utcnow()
    
    def is_locked(self) -> bool:
        """Verificar si la cuenta está bloqueada por intentos fallidos"""
        return self.failed_login_attempts >= 5
    
    def add_refresh_token(self, token: str):
        """Agregar token de refresh a la lista"""
        if token not in self.refresh_tokens:
            self.refresh_tokens.append(token)
            self.updated_at = datetime.utcnow()
    
    def remove_refresh_token(self, token: str):
        """Remover token de refresh"""
        if token in self.refresh_tokens:
            self.refresh_tokens.remove(token)
            self.updated_at = datetime.utcnow()
    
    def clear_all_refresh_tokens(self):
        """Limpiar todos los tokens de refresh"""
        self.refresh_tokens.clear()
        self.updated_at = datetime.utcnow()
    
    def verify_email(self):
        """Verificar email del usuario"""
        self.is_verified = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Desactivar cuenta"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        self.clear_all_refresh_tokens()
    
    def _register_event(self, event):
        """Registrar evento de dominio"""
        if not hasattr(self, '_events'):
            self._events = []
        self._events.append(event)
    
    def pull_events(self):
        """Obtener y limpiar eventos pendientes"""
        events = self._events.copy()
        self._events.clear()
        return events