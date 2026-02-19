from dataclasses import dataclass
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime

@dataclass
class QuestionDto:
    id: UUID
    apiary_id: UUID
    question_text: str
    question_type: str
    category: Optional[str] = None
    is_required: bool = False
    display_order: int = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    score: Optional[float] = None
    options: Optional[List[str]] = None
    depends_on: Optional[str] = None
    is_active: bool = True
    external_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class CreateQuestionDto:
    apiary_id: UUID
    question_text: str
    question_type: str
    category: Optional[str] = None
    is_required: bool = False
    display_order: int = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    score: Optional[float] = None
    options: Optional[List[str]] = None
    depends_on: Optional[str] = None
    is_active: bool = True
    external_id: Optional[str] = None

@dataclass
class UpdateQuestionDto:
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    category: Optional[str] = None
    is_required: Optional[bool] = None
    display_order: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    score: Optional[float] = None
    options: Optional[List[str]] = None
    depends_on: Optional[str] = None
    is_active: Optional[bool] = None
    external_id: Optional[str] = None
