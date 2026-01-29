from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID # Import UUID

@dataclass
class Apiary:
    id: UUID
    user_id: str
    name: str
    location: Optional[str]
    beehives_count: int = 0
    treatments: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
