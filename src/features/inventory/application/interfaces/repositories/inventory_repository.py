from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from src.features.inventory.domain.entities.inventory import Inventory


class InventoryRepository(ABC):
    @abstractmethod
    def get_low_stock(self, apiary_id: UUID) -> List[Inventory]:
        pass

    @abstractmethod
    def get_summary(self, apiary_id: UUID) -> Dict[str, Any]:
        pass

    @abstractmethod
    def search(self, apiary_id: UUID, query: str) -> List[Inventory]:
        pass

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
