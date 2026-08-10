from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from src.features.inventory.application.interfaces.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from src.features.inventory.domain.entities.inventory_movement import InventoryMovement
from src.features.inventory.infrastructure.models.inventory_movement_model import (
    InventoryMovementModel,
)
from src.features.inventory.application.mappers.inventory_movement_mapper import (
    InventoryMovementMapper,
)


class InventoryMovementRepositoryImpl(InventoryMovementRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_inventory_id(self, inventory_id: UUID) -> List[InventoryMovement]:
        models = (
            self.session.query(InventoryMovementModel)
            .filter(InventoryMovementModel.inventory_id == inventory_id)
            .order_by(InventoryMovementModel.created_at.desc())
            .all()
        )
        return [InventoryMovementMapper.to_entity(model) for model in models]

    def create(self, movement: InventoryMovement) -> InventoryMovement:
        model = InventoryMovementMapper.to_model(movement)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return InventoryMovementMapper.to_entity(model)
