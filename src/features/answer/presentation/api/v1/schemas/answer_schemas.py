from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class HiveAnswerResponseSchema(BaseModel):
    id: UUID
    hive_question_id: UUID
    answer: Optional[str] = None
    score: int = 0
    answered_by: Optional[UUID] = None
    answered_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    hive_question: Optional[object] = None

    class Config:
        from_attributes = True

class CreateAnswerRequestSchema(BaseModel):
    hive_question_id: UUID
    answer: str
    score: int = 0

class UpdateAnswerRequestSchema(BaseModel):
    answer: str
    score: Optional[int] = None

class BatchAnswerItemSchema(BaseModel):
    hive_question_id: UUID
    answer: str
    score: int = 0

class BatchCreateAnswersRequestSchema(BaseModel):
    answers: List[BatchAnswerItemSchema] = Field(..., min_items=1)

class BatchCreateAnswersResponseSchema(BaseModel):
    created: int
    answers: List[HiveAnswerResponseSchema]
