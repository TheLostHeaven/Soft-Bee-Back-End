from uuid import UUID, uuid4
from datetime import datetime
from src.features.inventory.application.dto.inventory_dto import RegisterMovementDTO
from src.features.inventory.application.interfaces.repositories.inventory_repository import InventoryRepository
from src.features.inventory.domain.entities.inventory import InventoryMovement
from src.features.inventory.domain.exceptions.inventory_exceptions import (
    InventoryNotFoundError,
    InvalidInventoryAdjustmentError,
)

class RegisterMovementUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, dto: RegisterMovementDTO) -> InventoryMovement:
        inventory = self.repository.get_by_id(dto.inventory_id)

        if not inventory:
            raise InventoryNotFoundError(dto.inventory_id)

        stock_before = inventory.quantity

        # Update inventory quantity
        if dto.movement_type == 'entry':
            inventory.quantity += dto.quantity
        elif dto.movement_type == 'exit':
            if inventory.quantity < dto.quantity:
                raise InvalidInventoryAdjustmentError(
                    f"Insufficient stock for {inventory.name}. Available: {inventory.quantity}, Requested: {dto.quantity}"
                )
            inventory.quantity -= dto.quantity
        else:
            raise ValueError(f"Invalid movement type: {dto.movement_type}")

        stock_after = inventory.quantity

        # Save movement with audit data
        movement = InventoryMovement(
            id=uuid4(),
            inventory_id=dto.inventory_id,
            movement_type=dto.movement_type,
            quantity=dto.quantity,
            stock_before=stock_before,
            stock_after=stock_after,
            reason=dto.reason,
            date=datetime.utcnow(),
            notes=dto.notes
        )
        
        self.repository.update(inventory)
        return self.repository.create_movement(movement)
