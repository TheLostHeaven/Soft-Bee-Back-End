from abc import ABC, abstractmethod
from typing import List, Dict, Any
from uuid import UUID  # Import UUID
from src.features.inventory.domain.entities.inventory import Inventory # Changed import to Inventory


class InventoryRepository(ABC):
    @abstractmethod
    def create_inventory(self, inventory_item: Inventory) -> Inventory: # Changed type to Inventory
        pass

    @abstractmethod
    def get_inventories_by_apiary(self, apiary_id: str) -> List[Inventory]: # Changed type to Inventory
        pass

    @abstractmethod
    def get_inventory_by_id(self, inventory_id: UUID) -> Inventory: # Changed inventory_id to UUID, return type to Inventory
        pass

    @abstractmethod
    def update_inventory(self, inventory_id: UUID, inventory_item: Inventory) -> Inventory: # Changed inventory_id to UUID, type to Inventory
        pass

    @abstractmethod
    def delete_inventory(self, inventory_id: UUID): # Changed inventory_id to UUID
        pass

    @abstractmethod
    def get_inventory_summary(self, apiary_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_low_stock_items(self, apiary_id: str) -> List[Inventory]: # Changed return type to Inventory
        pass

    @abstractmethod
    def adjust_inventory_quantity(self, item_id: UUID, amount: int): # Changed item_id to UUID
        pass

    @abstractmethod
    def search_inventory_items(self, apiary_id: str, query: str) -> List[Inventory]: # Changed return type to Inventory
        pass