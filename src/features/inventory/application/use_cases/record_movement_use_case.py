import uuid
from src.features.inventory.application.dto.inventory_movement_dto import CreateMovementDTO
from src.features.inventory.application.interfaces.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory_movement import InventoryMovement
from src.features.inventory.domain.exceptions.inventory_exceptions import (
    InventoryNotFoundError,
    InvalidInventoryAdjustmentError,
)


class RecordMovementUseCase:
    def __init__(
        self,
        inventory_repository: InventoryRepository,
        movement_repository: InventoryMovementRepository,
    ):
        self.inventory_repository = inventory_repository
        self.movement_repository = movement_repository

    def execute(self, dto: CreateMovementDTO) -> InventoryMovement:
        # Verify the inventory item exists
        inventory = self.inventory_repository.get_by_id(dto.inventory_id)
        if not inventory:
            raise InventoryNotFoundError(dto.inventory_id)

        # Calculate adjustment
        adjustment = dto.quantity if dto.movement_type == "entry" else -dto.quantity

        new_quantity = inventory.quantity + adjustment
        if new_quantity < 0:
            raise InvalidInventoryAdjustmentError(
                f"Exit of {dto.quantity} exceeds current stock ({inventory.quantity})."
            )

        # Update inventory quantity
        inventory.quantity = new_quantity
        self.inventory_repository.update(inventory)

        # Record the movement log
        movement = InventoryMovement(
            id=uuid.uuid4(),
            inventory_id=dto.inventory_id,
            movement_type=dto.movement_type,
            quantity=dto.quantity,
            notes=dto.notes,
        )
        saved_movement = self.movement_repository.create(movement)

        return saved_movement
