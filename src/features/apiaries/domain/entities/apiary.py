from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Apiary:
    id: int
    user_id: str
    name: str
    location: Optional[str]
    beehives_count: int = 0
    treatments: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
