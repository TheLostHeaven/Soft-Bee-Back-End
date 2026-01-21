from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, Dict, Any

class LoginRequestDTO(BaseModel):
    """DTO para request de login"""
    email: EmailStr
    password: str = Field(..., min_length=1, description="Password del usuario")
    remember_me: bool = Field(default=False, description="Recordar sesión")

class LoginResponseDTO(BaseModel):
    """DTO para response de login"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class RegisterRequestDTO(BaseModel):
    """DTO para request de registro"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username can only contain letters, numbers and underscores')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class RegisterResponseDTO(BaseModel):
    """DTO para response de registro"""
    id: str
    email: str
    username: str
    is_verified: bool
    created_at: datetime
    message: str = "User registered successfully"

class RefreshTokenRequestDTO(BaseModel):
    """DTO para request de refresh token"""
    refresh_token: str

class RefreshTokenResponseDTO(BaseModel):
    """DTO para response de refresh token"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int

class LogoutRequestDTO(BaseModel):
    """DTO para request de logout"""
    refresh_token: Optional[str] = None

class VerifyTokenRequestDTO(BaseModel):
    """DTO para request de verificación de token"""
    token: str

class VerifyTokenResponseDTO(BaseModel):
    """DTO para response de verificación de token"""
    is_valid: bool
    user_id: Optional[str] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None