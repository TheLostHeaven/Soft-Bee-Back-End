from pydantic import BaseModel, EmailStr, Field, validator, field_validator
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
        from_attributes = True

# Schema para respuesta de auth
class AuthResponseSchema(BaseModel):
    """Schema para respuestas de auth"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponseSchema



class ForgotPasswordSchema(BaseModel):
    """Schema para solicitar reseteo de contraseña"""
    email: EmailStr
        
    class Config:
            json_schema_extra = {
                "example": {
                    "email": "usuario@ejemplo.com"
                }
            }


class ResetPasswordSchema(BaseModel):
    """Schema para confirmar reseteo de contraseña"""
    token: str = Field(..., min_length=32, max_length=32, 
                    description="Token de reseteo (32 caracteres)")
    new_password: str = Field(..., min_length=8, max_length=100,
                            description="Nueva contraseña (mínimo 8 caracteres)")
    
    @field_validator('token')
    @classmethod
    def validate_token_length(cls, v: str) -> str:
        if len(v) != 32:
            raise ValueError('Token must be exactly 32 characters')
        return v
    
    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Puedes agregar más validaciones aquí si lo deseas
        # Ejemplo: validar fortaleza de contraseña
        # if not any(char.isdigit() for char in v):
        #     raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "abc123def456ghi789jkl012mno345pqr",
                "new_password": "NuevaContraseñaSegura123"
            }
        }

class ResetPasswordResponseSchema(BaseModel):
    """Schema para respuesta de reseteo de contraseña"""
    success: bool
    message: str
    user_id: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Password has been reset successfully",
                "user_id": "uuid-usuario",
                "email": "usuario@ejemplo.com"
            }
        }