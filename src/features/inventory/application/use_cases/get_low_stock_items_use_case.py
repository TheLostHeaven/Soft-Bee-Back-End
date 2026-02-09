from typing import List
from src.features.inventory.domain.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory


class GetLowStockItemsUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, apiary_id: str) -> List[Inventory]:
        return self.repository.get_low_stock_items(apiary_id)
