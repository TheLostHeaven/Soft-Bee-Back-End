from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID

@dataclass
class Question:
    id: Optional[UUID]
    apiary_id: UUID
    question_text: str
    question_type: str  # 'texto', 'numero', 'opciones', 'rango'
    external_id: Optional[str] = None
    category: Optional[str] = None
    is_required: bool = False
    display_order: int = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    options: Optional[List[str]] = None
    depends_on: Optional[UUID] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
