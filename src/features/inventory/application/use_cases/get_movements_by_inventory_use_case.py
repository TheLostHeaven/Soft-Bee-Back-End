from typing import List
from uuid import UUID

from src.features.inventory.application.interfaces.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from src.features.inventory.domain.entities.inventory_movement import InventoryMovement


class GetMovementsByInventoryUseCase:
    def __init__(self, movement_repository: InventoryMovementRepository):
        self.movement_repository = movement_repository

    def execute(self, inventory_id: UUID) -> List[InventoryMovement]:
        return self.movement_repository.get_by_inventory_id(inventory_id)
