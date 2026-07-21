from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Inventory:
    id: UUID
    apiary_id: UUID
    name: str
    quantity: int
    unit: str
    description: Optional[str]
    minimum_stock: int
    created_at: datetime
    updated_at: datetime
    category: str = "General"
