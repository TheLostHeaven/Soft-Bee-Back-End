from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.features.inventory.domain.entities.inventory_movement import InventoryMovement


class InventoryMovementRepository(ABC):
    @abstractmethod
    def get_by_inventory_id(self, inventory_id: UUID) -> List[InventoryMovement]:
        pass

    @abstractmethod
    def create(self, movement: InventoryMovement) -> InventoryMovement:
        pass
