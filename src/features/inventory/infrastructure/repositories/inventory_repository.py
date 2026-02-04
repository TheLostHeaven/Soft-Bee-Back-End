from typing import List, Optional
from sqlalchemy.orm import Session
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory
from src.features.inventory.infrastructure.models.inventory_model import InventoryModel
from src.features.inventory.application.mappers.inventory_mapper import InventoryMapper
from uuid import UUID


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, apiary_id: UUID) -> List[Inventory]:
        models = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.apiary_id == apiary_id)
            .all()
        )
        return [InventoryMapper.to_entity(model) for model in models]

    def get_by_id(self, inventory_id: UUID) -> Optional[Inventory]:
        model = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.id == inventory_id)
            .first()
        )
        return InventoryMapper.to_entity(model) if model else None

    def create(self, inventory: Inventory) -> Inventory:
        model = InventoryMapper.to_model(inventory)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return InventoryMapper.to_entity(model)

    def update(self, inventory: Inventory) -> Inventory:
        model = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.id == inventory.id)
            .first()
        )
        if model:
            model.name = inventory.name
            model.quantity = inventory.quantity
            model.unit = inventory.unit
            model.description = inventory.description
            model.minimum_stock = inventory.minimum_stock
            self.session.commit()
            self.session.refresh(model)
            return InventoryMapper.to_entity(model)
        return None

    def delete(self, inventory_id: UUID) -> None:
        model = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.id == inventory_id)
            .first()
        )
        if model:
            self.session.delete(model)
            self.session.commit()
