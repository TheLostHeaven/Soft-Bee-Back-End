from typing import List
from src.features.inventory.domain.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory


class SearchInventoryItemsUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, apiary_id: str, query: str) -> List[Inventory]:
        return self.repository.search_inventory_items(apiary_id, query)
