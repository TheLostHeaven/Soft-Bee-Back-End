from uuid import UUID

from src.features.inventory.application.dto.adjust_inventory_quantity_dto import (
    AdjustInventoryQuantityDTO,
)
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory


class AdjustInventoryQuantityUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID, dto: AdjustInventoryQuantityDTO) -> Inventory:
        inventory = self.repository.get_by_id(inventory_id)
        if not inventory:
            raise Exception("Inventory not found")

        inventory.quantity += dto.amount

        return self.repository.update(inventory)