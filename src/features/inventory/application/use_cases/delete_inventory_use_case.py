from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from uuid import UUID
from src.features.inventory.domain.exceptions.inventory_exceptions import InventoryNotFoundException


class DeleteInventoryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID) -> None:
        inventory = self.repository.get_inventory_by_id(inventory_id)
        if not inventory:
            raise InventoryNotFoundException(f"Inventory with id {inventory_id} not found")
        self.repository.delete_inventory(inventory_id)
