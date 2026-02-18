from pydantic import BaseModel
from typing import List
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.inventory.application.dto.inventory_dto import InventoryDTO

class ApiaryInventorySummaryDTO(BaseModel):
    apiary: ApiaryDto
    inventories: List[InventoryDTO]

    class Config:
        from_attributes = True

class InventorySummaryDTO(BaseModel):
    summary: List[ApiaryInventorySummaryDTO]

    class Config:
        from_attributes = True
