from src.features.inventory.domain.entities.inventory_movement import InventoryMovement
from src.features.inventory.infrastructure.models.inventory_movement_model import (
    InventoryMovementModel,
)
from src.features.inventory.application.dto.inventory_movement_dto import (
    InventoryMovementDTO,
)


class InventoryMovementMapper:
    @staticmethod
    def to_dto(movement: InventoryMovement) -> InventoryMovementDTO:
        return InventoryMovementDTO(
            id=movement.id,
            inventory_id=movement.inventory_id,
            movement_type=movement.movement_type,
            quantity=movement.quantity,
            notes=movement.notes,
            created_at=movement.created_at,
        )

    @staticmethod
    def to_entity(model: InventoryMovementModel) -> InventoryMovement:
        return InventoryMovement(
            id=model.id,
            inventory_id=model.inventory_id,
            movement_type=model.movement_type,
            quantity=model.quantity,
            notes=model.notes,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(movement: InventoryMovement) -> InventoryMovementModel:
        return InventoryMovementModel(
            id=movement.id,
            inventory_id=movement.inventory_id,
            movement_type=movement.movement_type,
            quantity=movement.quantity,
            notes=movement.notes,
        )
