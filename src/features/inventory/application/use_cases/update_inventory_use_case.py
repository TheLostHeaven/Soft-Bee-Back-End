from src.features.inventory.application.dto.inventory_dto import UpdateInventoryDTO
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory
from uuid import UUID


class UpdateInventoryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID, dto: UpdateInventoryDTO) -> Inventory:
        inventory = self.repository.get_by_id(inventory_id)
        if not inventory:
            raise Exception("Inventory not found")

        update_data = dto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(inventory, key, value)

        return self.repository.update(inventory)
