# src/features/auth/presentation/api/v1/schemas/auth_schemas.py - VERSIÓN PYDANTIC
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class LoginSchema(BaseModel):
    """Schema para login usando Pydantic"""
    email: EmailStr
    password: str = Field(..., min_length=1)
    remember_me: bool = False

class RegisterSchema(BaseModel):
    """Schema para registro usando Pydantic"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validar fortaleza del password"""
        import re
        if not re.search(r'[A-Z]', v):
            raise ValueError('Must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Must contain number')
        if not re.search(r'[^A-Za-z0-9]', v):
            raise ValueError('Must contain special character')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Verificar que los passwords coincidan"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class RefreshTokenSchema(BaseModel):
    """Schema para refresh token"""
    refresh_token: str

class LogoutSchema(BaseModel):
    """Schema para logout"""
    refresh_token: Optional[str] = None

class VerifyTokenSchema(BaseModel):
    """Schema para verificar token"""
    token: str

# Schema para respuesta de usuario
class UserResponseSchema(BaseModel):
    """Schema para serializar usuario (response)"""
    id: str
    email: str
    username: str
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Permite crear desde ORM objects

# Schema para respuesta de auth
class AuthResponseSchema(BaseModel):
    """Schema para respuestas de auth"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponseSchema