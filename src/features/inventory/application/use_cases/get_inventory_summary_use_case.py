from typing import Dict, Any
from uuid import UUID

from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)


class GetInventorySummaryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, apiary_id: UUID) -> Dict[str, Any]:
        return self.repository.get_summary(apiary_id)
