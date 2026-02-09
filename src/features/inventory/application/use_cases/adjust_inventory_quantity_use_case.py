from src.features.inventory.domain.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.application.dto.adjust_inventory_quantity_dto import (
    AdjustInventoryQuantityDTO,
)


class AdjustInventoryQuantityUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, dto: AdjustInventoryQuantityDTO):
        self.repository.adjust_inventory_quantity(dto.item_id, dto.amount)
