import re
from dataclasses import dataclass, field
from typing import Optional
from ...domain.exceptions.auth_exceptions import InvalidEmailException

@dataclass(frozen=True)
class Email:
    """Value Object para email"""
    value: str
    
    def __post_init__(self):
        # Normalizar a minúsculas antes de cualquier otra operación
        # Necesitamos 'engañar' a un objeto frozen para poder modificarlo
        object.__setattr__(self, 'value', self.value.lower())
        
        if not self.is_valid():
            raise InvalidEmailException(f"Invalid email address: {self.value}")
    
    def is_valid(self) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return bool(re.match(pattern, self.value))
    
    def get_domain(self) -> str:
        """Obtener dominio del email"""
        return self.value.split('@')[1] if '@' in self.value else ''
    
    def get_username(self) -> str:
        """Obtener nombre de usuario del email"""
        return self.value.split('@')[0] if '@' in self.value else ''
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Email):
            return self.value == other.value
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)