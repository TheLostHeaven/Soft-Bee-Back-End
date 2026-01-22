from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApiaryDto(BaseModel):
    id: int
    user_id: str
    name: str
    location: Optional[str]
    beehives_count: int
    treatments: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CreateApiaryDto(BaseModel):
    user_id: str
    name: str
    location: Optional[str] = None
    beehives_count: int = 0
    treatments: bool = False

class UpdateApiaryDto(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    beehives_count: Optional[int] = None
    treatments: Optional[bool] = None
