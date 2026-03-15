from uuid import UUID
from src.features.inventory.application.dto.inventory_dto import AdjustInventoryDTO
from src.features.inventory.application.interfaces.repositories.inventory_repository import InventoryRepository
from src.features.inventory.domain.entities.inventory import Inventory
from src.features.inventory.domain.exceptions.inventory_exceptions import (
    InventoryNotFoundError,
    InvalidInventoryAdjustmentError,
)

class AdjustInventoryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID, dto: AdjustInventoryDTO, reason: str = "Ajuste manual", notes: str = None) -> Inventory:
        inventory = self.repository.get_by_id(inventory_id)

        if not inventory:
            raise InventoryNotFoundError(inventory_id)

        stock_before = inventory.quantity
        new_quantity = stock_before + dto.adjustment_amount

        if new_quantity < 0:
            raise InvalidInventoryAdjustmentError(
                f"Adjustment of {dto.adjustment_amount} results in a negative quantity ({new_quantity})."
            )

        inventory.quantity = new_quantity
        updated_inventory = self.repository.update(inventory)
        
        # Record the movement in history
        self.repository.record_movement(
            inventory_id=inventory_id,
            movement_type='entry' if dto.adjustment_amount > 0 else 'exit',
            quantity=abs(dto.adjustment_amount),
            stock_before=stock_before,
            stock_after=new_quantity,
            reason=reason,
            notes=notes
        )
        
        return updated_inventory
