from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from uuid import UUID


class DeleteInventoryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID) -> None:
        inventory = self.repository.get_by_id(inventory_id)
        if not inventory:
            raise Exception("Inventory not found")
        return self.repository.delete(inventory_id)
