from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ApiaryQuestionResponseSchema(BaseModel):
    id: UUID
    apiary_id: UUID
    question_id: str
    category: str
    question: str
    type: str
    display_order: int
    is_required: bool
    options: Optional[str] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    depends_on: Optional[str] = None
    is_active: bool
    is_system: bool
    score: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class HiveQuestionResponseSchema(BaseModel):
    id: UUID
    hive_id: UUID
    apiary_question_id: UUID
    display_order: int
    is_active: bool
    assigned_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    apiary_question: Optional[ApiaryQuestionResponseSchema] = None

    class Config:
        from_attributes = True

class CreateApiaryQuestionRequestSchema(BaseModel):
    apiary_id: UUID
    question_id: Optional[str] = None
    category: str
    question: str
    type: str
    display_order: int = 0
    is_required: bool = False
    options: Optional[str] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    depends_on: Optional[str] = None
    score: int = 0

class AssignQuestionToHiveRequestSchema(BaseModel):
    hive_id: UUID
    apiary_question_id: UUID
    display_order: int = Field(..., ge=1)

class UpdateHiveQuestionRequestSchema(BaseModel):
    is_active: Optional[bool] = None
    display_order: Optional[int] = None
