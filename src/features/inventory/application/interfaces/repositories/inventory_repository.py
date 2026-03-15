from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.features.inventory.domain.entities.inventory import Inventory


class InventoryRepository(ABC):
    @abstractmethod
    def get_all(self, apiary_id: UUID) -> List[Inventory]:
        pass

    @abstractmethod
    def get_by_id(self, inventory_id: UUID) -> Optional[Inventory]:
        pass

    @abstractmethod
    def create(self, inventory: Inventory) -> Inventory:
        pass

    @abstractmethod
    def update(self, inventory: Inventory) -> Inventory:
        pass

    @abstractmethod
    def delete(self, inventory_id: UUID) -> None:
        pass

    @abstractmethod
    def record_movement(self, inventory_id: UUID, movement_type: str, quantity: int, stock_before: int, stock_after: int, reason: str = None, notes: str = None) -> None:
        pass

    @abstractmethod
    def get_movements(self, inventory_id: UUID) -> List[dict]:
        pass
