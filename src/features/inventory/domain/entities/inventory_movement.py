from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class InventoryMovement:
    id: UUID
    inventory_id: UUID
    movement_type: str  # "entry" or "exit"
    quantity: int
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
