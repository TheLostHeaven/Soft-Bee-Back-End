from typing import Dict
from src.features.inventory.domain.repositories.inventory_repository import (
    InventoryRepository,
)


class GetInventorySummaryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, apiary_id: str) -> Dict[str, any]:
        return self.repository.get_inventory_summary(apiary_id)
