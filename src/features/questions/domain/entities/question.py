from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class ApiaryQuestion:
    id: UUID
    apiary_id: UUID
    question_id: str
    category: str
    question: str
    type: str
    display_order: int
    is_required: bool = False
    options: Optional[str] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    depends_on: Optional[str] = None
    is_active: bool = True
    is_system: bool = False
    score: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class HiveQuestion:
    id: UUID
    hive_id: UUID
    apiary_question_id: UUID
    display_order: int
    is_active: bool = True
    assigned_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Optional field to hold detailed info from ApiaryQuestion
    apiary_question: Optional[ApiaryQuestion] = None
