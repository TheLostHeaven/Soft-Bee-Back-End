from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from src.core.database.db import db
from src.features.inventory.infrastructure.models.inventory_model import InventoryModel
from src.features.inventory.domain.entities.inventory import Inventory
from sqlalchemy import func
from datetime import datetime


class InventorySQLDataSource:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _model_to_entity(self, model: InventoryModel) -> Inventory:
        return Inventory(
            id=model.id,
            apiary_id=model.apiary_id,
            name=model.name,
            quantity=model.quantity,
            unit=model.unit,
            description=model.description,
            minimum_stock=model.minimum_stock,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model(self, entity: Inventory) -> InventoryModel:
        return InventoryModel(
            id=entity.id,
            apiary_id=entity.apiary_id,
            name=entity.name,
            quantity=entity.quantity,
            unit=entity.unit,
            description=entity.description,
            minimum_stock=entity.minimum_stock,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def create_inventory(self, inventory_entity: Inventory) -> Inventory:
        try:
            new_inventory_model = self._entity_to_model(inventory_entity)
            self.db_session.add(new_inventory_model)
            self.db_session.flush()
            self.db_session.commit()
            return self._model_to_entity(new_inventory_model)
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_inventories_by_apiary(self, apiary_id: UUID) -> List[Inventory]:
        inventory_models = (
            self.db_session.query(InventoryModel)
            .filter_by(apiary_id=apiary_id)
            .all()
        )
        return [self._model_to_entity(model) for model in inventory_models]

    def get_inventory_by_id(self, inventory_id: UUID) -> Inventory:
        inventory_model = (
            self.db_session.query(InventoryModel)
            .filter_by(id=inventory_id)
            .first()
        )
        return self._model_to_entity(inventory_model) if inventory_model else None

    def update_inventory(self, inventory_id: UUID, inventory_entity: Inventory) -> Inventory:
        try:
            inventory_model = (
                self.db_session.query(InventoryModel)
                .filter_by(id=inventory_id)
                .first()
            )
            if not inventory_model:
                raise ValueError(f"Inventory with id {inventory_id} not found.")

            inventory_model.name = inventory_entity.name
            inventory_model.quantity = inventory_entity.quantity
            inventory_model.unit = inventory_entity.unit
            inventory_model.description = inventory_entity.description
            inventory_model.minimum_stock = inventory_entity.minimum_stock
            inventory_model.updated_at = datetime.utcnow()

            self.db_session.add(inventory_model)
            self.db_session.flush()
            self.db_session.commit()
            return self._model_to_entity(inventory_model)
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_inventory(self, inventory_id: UUID):
        try:
            inventory_model = (
                self.db_session.query(InventoryModel)
                .filter_by(id=inventory_id)
                .first()
            )
            if not inventory_model:
                raise ValueError(f"Inventory with id {inventory_id} not found.")
            self.db_session.delete(inventory_model)
            self.db_session.flush()
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_inventory_summary(self, apiary_id: UUID) -> Dict[str, Any]:
        total_items_query = (
            self.db_session.query(func.count(InventoryModel.id))
            .filter_by(apiary_id=apiary_id)
            .scalar()
        )
        total_quantity_query = (
            self.db_session.query(func.sum(InventoryModel.quantity))
            .filter_by(apiary_id=apiary_id)
            .scalar()
        )
        low_stock_items_query = (
            self.db_session.query(func.count(InventoryModel.id))
            .filter_by(apiary_id=apiary_id)
            .filter(InventoryModel.quantity <= InventoryModel.minimum_stock)
            .scalar()
        )
        out_of_stock_items_query = (
            self.db_session.query(func.count(InventoryModel.id))
            .filter_by(apiary_id=apiary_id)
            .filter(InventoryModel.quantity == 0)
            .scalar()
        )
        
        # Considerar el caso donde no hay items para evitar errores de división por cero
        if total_items_query == 0:
            average_stock = 0.0
        else:
            average_stock = (total_quantity_query or 0) / total_items_query

        return {
            "total_items": total_items_query,
            "total_quantity": total_quantity_query,
            "low_stock_items": low_stock_items_query,
            "out_of_stock_items": out_of_stock_items_query,
            "average_stock": average_stock,
        }


    def get_low_stock_items(self, apiary_id: UUID) -> List[Inventory]:
        low_stock_models = (
            self.db_session.query(InventoryModel)
            .filter_by(apiary_id=apiary_id)
            .filter(InventoryModel.quantity <= InventoryModel.minimum_stock)
            .all()
        )
        return [self._model_to_entity(model) for model in low_stock_models]

    def adjust_inventory_quantity(self, item_id: UUID, amount: int):
        inventory_model = (
            self.db_session.query(InventoryModel)
            .filter_by(id=item_id)
            .first()
        )
        if not inventory_model:
            raise ValueError(f"Inventory with id {item_id} not found.")
        inventory_model.quantity += amount
        if inventory_model.quantity < 0:
            inventory_model.quantity = 0 # Evitar cantidades negativas
        self.db_session.add(inventory_model)
        self.db_session.flush()

    def search_inventory_items(self, apiary_id: UUID, query: str) -> List[Inventory]:
        search_query = f"%{query.lower()}%"
        inventory_models = (
            self.db_session.query(InventoryModel)
            .filter_by(apiary_id=apiary_id)
            .filter(InventoryModel.name.ilike(search_query)) # ilike para búsqueda insensible a mayúsculas/minúsculas
            .all()
        )
        return [self._model_to_entity(model) for model in inventory_models]
