# src/features/auth/application/dto/reset_password_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ForgotPasswordRequestDTO:
    """DTO para solicitar reseteo de contraseña"""
    email: str

@dataclass
class ResetPasswordConfirmDTO:
    """DTO para confirmar reseteo de contraseña"""
    token: str
    new_password: str

@dataclass
class PasswordResetResultDTO:
    """DTO para resultado del reseteo de contraseña"""
    success: bool
    message: str
    user_id: Optional[str] = None
    email: Optional[str] = None