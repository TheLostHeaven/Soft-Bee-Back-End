from typing import List, Optional, Dict, Any
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

    def get_low_stock(self, apiary_id: UUID) -> List[Inventory]:
        models = (
            self.session.query(InventoryModel)
            .filter(
                InventoryModel.apiary_id == apiary_id,
                InventoryModel.quantity <= InventoryModel.minimum_stock,
                InventoryModel.quantity > 0, # Consider only items that are not out of stock
            )
            .all()
        )
        return [InventoryMapper.to_entity(model) for model in models]

    def get_summary(self, apiary_id: UUID) -> Dict[str, Any]:
        inventory_items = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.apiary_id == apiary_id)
            .all()
        )

        total_items = len(inventory_items)
        total_quantity = sum(item.quantity for item in inventory_items)
        in_stock_items = sum(1 for item in inventory_items if item.quantity > 0)
        out_of_stock_items = sum(1 for item in inventory_items if item.quantity <= 0)
        low_stock_items = sum(
            1 for item in inventory_items if 0 < item.quantity <= item.minimum_stock
        )
        updated_at = (
            max(item.updated_at for item in inventory_items)
            if inventory_items
            else None
        )

        return {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "in_stock_items": in_stock_items,
            "out_of_stock_items": out_of_stock_items,
            "low_stock_items": low_stock_items,
            "updated_at": updated_at.isoformat() if updated_at else None,
        }


    def search(self, apiary_id: UUID, query: str) -> List[Inventory]:
        models = (
            self.session.query(InventoryModel)
            .filter(
                InventoryModel.apiary_id == apiary_id,
                InventoryModel.name.ilike(f"%{query}%"),
            )
            .all()
        )
        return [InventoryMapper.to_entity(model) for model in models]

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