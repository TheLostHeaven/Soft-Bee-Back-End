from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ApiaryResponseSchema(BaseModel):
    id: UUID
    user_id: str
    name: str
    location: Optional[str]
    beehives_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CreateApiaryRequestSchema(BaseModel):
    user_id: str
    name: str
    location: Optional[str] = None
    beehives_count: int = 0

class UpdateApiaryRequestSchema(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    beehives_count: Optional[int] = None
