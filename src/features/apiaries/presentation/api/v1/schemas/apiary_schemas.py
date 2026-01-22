from pydantic import BaseModel
from typing import Optional

class ApiaryResponseSchema(BaseModel):
    id: int
    user_id: str
    name: str
    location: Optional[str]
    beehives_count: int
    treatments: bool

    class Config:
        from_attributes = True

class CreateApiaryRequestSchema(BaseModel):
    user_id: str
    name: str
    location: Optional[str] = None
    beehives_count: int = 0
    treatments: bool = False

class UpdateApiaryRequestSchema(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    beehives_count: Optional[int] = None
    treatments: Optional[bool] = None
