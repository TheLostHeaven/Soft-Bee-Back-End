from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class HiveAnswer:
    id: UUID
    hive_question_id: UUID
    answer: Optional[str] = None
    score: int = 0
    answered_by: Optional[UUID] = None
    answered_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Optional field to hold detailed info from HiveQuestion
    hive_question: Optional[object] = None  # Will be HiveQuestion from questions feature
    user: Optional[object] = None  # Will be User from user feature
