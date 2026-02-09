from typing import List, Dict, Any
from uuid import UUID
from src.features.inventory.domain.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory
from src.features.inventory.infrastructure.datasources.inventory_sql_datasource import (
    InventorySQLDataSource,
)


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self, datasource: InventorySQLDataSource):
        self.datasource = datasource

    def create_inventory(self, inventory_entity: Inventory) -> Inventory:
        return self.datasource.create_inventory(inventory_entity)

    def get_inventories_by_apiary(self, apiary_id: UUID) -> List[Inventory]:
        return self.datasource.get_inventories_by_apiary(apiary_id)

    def get_inventory_by_id(self, inventory_id: UUID) -> Inventory:
        return self.datasource.get_inventory_by_id(inventory_id)

    def update_inventory(self, inventory_id: UUID, inventory_entity: Inventory) -> Inventory:
        return self.datasource.update_inventory(inventory_id, inventory_entity)

    def delete_inventory(self, inventory_id: UUID):
        self.datasource.delete_inventory(inventory_id)

    def get_inventory_summary(self, apiary_id: UUID) -> Dict[str, Any]:
        return self.datasource.get_inventory_summary(apiary_id)

    def get_low_stock_items(self, apiary_id: UUID) -> List[Inventory]:
        return self.datasource.get_low_stock_items(apiary_id)

    def adjust_inventory_quantity(self, item_id: UUID, amount: int):
        self.datasource.adjust_inventory_quantity(item_id, amount)

    def search_inventory_items(self, apiary_id: UUID, query: str) -> List[Inventory]:
        return self.datasource.search_inventory_items(apiary_id, query)
