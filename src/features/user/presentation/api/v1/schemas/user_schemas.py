from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserResponseSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    photo_url: Optional[str] = None

class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    photo_url: Optional[str] = None
