from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class QuestionDto(BaseModel):
    id: UUID
    apiary_id: UUID
    question_text: str
    question_type: str
    category: Optional[str] = None
    is_required: bool = False
    display_order: int = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    options: Optional[List[str]] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CreateQuestionDto(BaseModel):
    apiary_id: UUID
    question_text: str
    question_type: str
    category: Optional[str] = None
    is_required: bool = False
    display_order: int = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    options: Optional[List[str]] = None

class UpdateQuestionDto(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    category: Optional[str] = None
    is_required: Optional[bool] = None
    display_order: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    options: Optional[List[str]] = None
    is_active: Optional[bool] = None
