from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from src.features.user.application.dto.user_dto import UserDTO
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.beehive.application.dto.beehive_dto import BeehiveDTO
from src.features.inventory.application.dto.inventory_dto import InventoryDTO

class ApiaryFullDataDTO(ApiaryDto):
    beehives: List[BeehiveDTO] = []
    inventory: List[InventoryDTO] = []

class UserFullDataDTO(BaseModel):
    user: UserDTO
    apiaries: List[ApiaryFullDataDTO] = []

    class Config:
        from_attributes = True
