from typing import List
from uuid import UUID
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory


class GetInventoriesByApiaryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, apiary_id: UUID) -> List[Inventory]:
        return self.repository.get_inventories_by_apiary(apiary_id)
