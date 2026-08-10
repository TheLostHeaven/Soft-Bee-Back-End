from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class InventoryMovementDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    inventory_id: UUID
    movement_type: str
    quantity: int
    notes: Optional[str] = None
    created_at: datetime


class CreateMovementDTO(BaseModel):
    inventory_id: UUID
    movement_type: str  # "entry" or "exit"
    quantity: int
    notes: Optional[str] = None
