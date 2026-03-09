from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class HiveAnswerDto(BaseModel):
    id: UUID
    hive_question_id: UUID
    answer: Optional[str] = None
    score: int = 0
    answered_by: Optional[UUID] = None
    answered_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    hive_question: Optional[object] = None  # HiveQuestionDto
    user: Optional[object] = None  # UserDto

    class Config:
        from_attributes = True
