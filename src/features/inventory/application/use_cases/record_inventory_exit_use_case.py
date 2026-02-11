from uuid import UUID

from src.features.inventory.application.dto.record_inventory_exit_dto import (
    RecordInventoryExitDTO,
)
from src.features.inventory.application.use_cases.adjust_inventory_quantity_use_case import (
    AdjustInventoryQuantityUseCase,
)
from src.features.inventory.application.dto.adjust_inventory_quantity_dto import ( # Import AdjustInventoryQuantityDTO
    AdjustInventoryQuantityDTO,
)
from src.features.inventory.domain.entities.inventory import Inventory


class RecordInventoryExitUseCase:
    def __init__(self, adjust_inventory_quantity_use_case: AdjustInventoryQuantityUseCase):
        self.adjust_inventory_quantity_use_case = adjust_inventory_quantity_use_case

    def execute(self, dto: RecordInventoryExitDTO) -> Inventory:
        # Reutilizar AdjustInventoryQuantityUseCase con cantidad negativa
        adjust_dto = AdjustInventoryQuantityDTO( # Usar el DTO importado
            amount=-dto.quantity
        )
        return self.adjust_inventory_quantity_use_case.execute(dto.item_id, adjust_dto)
