from dataclasses import dataclass
from datetime import datetime
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
    
    # Campos Profesionales
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    supplier: Optional[str] = None
    storage_location: Optional[str] = None
    
    created_at: datetime = None
    updated_at: datetime = None
