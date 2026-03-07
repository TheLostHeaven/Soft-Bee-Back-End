from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from uuid import UUID


@dataclass
class Inventory:
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
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class InventoryMovement:
    id: UUID
    inventory_id: UUID
    movement_type: str # 'entry', 'exit'
    quantity: int
    stock_before: int
    stock_after: int
    reason: str
    date: datetime
    notes: Optional[str]
