from pydantic import BaseModel, EmailStr, Field, validator, field_validator # Added field_validator
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

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
    user_id: str 
    email: str
    username: str

class RegisterRequestDTO(BaseModel):
    """DTO para request de registro"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username can only contain letters, numbers and underscores')
        return v
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info): # Changed 'values' to 'info'
        if 'password' in info.data and v != info.data['password']: # Access values via info.data
            raise ValueError('Passwords do not match')
        return v

class RegisterResponseDTO(BaseModel):
    """DTO para response de registro"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str 
    email: str
    username: str

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