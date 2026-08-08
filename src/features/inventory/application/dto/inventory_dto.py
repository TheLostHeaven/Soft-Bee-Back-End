from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class InventoryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    apiary_id: UUID
    name: str
    category: str = "General"
    quantity: int
    unit: str
    description: Optional[str]
    minimum_stock: int
    created_at: datetime
    updated_at: datetime


class CreateInventoryDTO(BaseModel):
    apiary_id: UUID
    name: str
    category: str = "General"
    quantity: int
    unit: str
    description: Optional[str]
    minimum_stock: int


class UpdateInventoryDTO(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    description: Optional[str] = None
    minimum_stock: Optional[int] = None


class AdjustInventoryDTO(BaseModel):
    adjustment_amount: int
