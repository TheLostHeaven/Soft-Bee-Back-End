from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID


class InventoryDTO(BaseModel):
    id: UUID
    apiary_id: UUID
    name: str
    category: str
    quantity: int
    unit: str
    description: Optional[str]
    minimum_stock: int
    
    # Nuevos campos
    batch_number: Optional[str] = None
    expiry_date: Optional[date] = None
    purchase_date: Optional[date] = None
    supplier: Optional[str] = None
    storage_location: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateInventoryDTO(BaseModel):
    apiary_id: UUID
    name: str
    category: str = "General"
    quantity: int
    unit: str
    description: Optional[str] = None
    minimum_stock: int = 0
    batch_number: Optional[str] = None
    expiry_date: Optional[date] = None
    purchase_date: Optional[date] = None
    supplier: Optional[str] = None
    storage_location: Optional[str] = None


class UpdateInventoryDTO(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    description: Optional[str] = None
    minimum_stock: Optional[int] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[date] = None
    purchase_date: Optional[date] = None
    supplier: Optional[str] = None
    storage_location: Optional[str] = None


class AdjustInventoryDTO(BaseModel):
    adjustment_amount: int
    reason: str = "adjustment"
    notes: Optional[str] = None

class InventoryMovementDTO(BaseModel):
    id: UUID
    inventory_id: UUID
    movement_type: str
    quantity: int
    stock_before: int
    stock_after: int
    reason: str
    date: datetime
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class RegisterMovementDTO(BaseModel):
    inventory_id: UUID
    movement_type: str # 'entry', 'exit'
    quantity: int
    reason: str
    notes: Optional[str] = None
