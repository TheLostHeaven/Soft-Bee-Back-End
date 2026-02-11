from typing import Optional
from uuid import UUID

from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory


class GetInventoryItemUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID) -> Optional[Inventory]:
        return self.repository.get_by_id(inventory_id)
