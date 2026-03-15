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
        
        # Record creation movement
        self.record_movement(
            inventory_id=model.id,
            movement_type='create',
            quantity=model.quantity,
            stock_before=0,
            stock_after=model.quantity,
            reason='Creación inicial'
        )
        
        return InventoryMapper.to_entity(model)

    def update(self, inventory: Inventory) -> Inventory:
        model = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.id == inventory.id)
            .first()
        )
        if model:
            stock_before = model.quantity
            
            model.name = inventory.name
            model.category = inventory.category
            model.quantity = inventory.quantity
            model.unit = inventory.unit
            model.description = inventory.description
            model.minimum_stock = inventory.minimum_stock
            
            # Update professional fields
            model.batch_number = inventory.batch_number
            model.expiry_date = inventory.expiry_date
            model.purchase_date = inventory.purchase_date
            model.supplier = inventory.supplier
            model.storage_location = inventory.storage_location

            self.session.commit()
            self.session.refresh(model)
            
            if stock_before != model.quantity:
                self.record_movement(
                    inventory_id=model.id,
                    movement_type='update',
                    quantity=model.quantity - stock_before,
                    stock_before=stock_before,
                    stock_after=model.quantity,
                    reason='Actualización de stock'
                )
            else:
                # Still record an update movement even if quantity didn't change (e.g. edited name)
                self.record_movement(
                    inventory_id=model.id,
                    movement_type='update',
                    quantity=0,
                    stock_before=stock_before,
                    stock_after=model.quantity,
                    reason='Actualización de información'
                )
            
            return InventoryMapper.to_entity(model)
        return None

    def delete(self, inventory_id: UUID) -> None:
        model = (
            self.session.query(InventoryModel)
            .filter(InventoryModel.id == inventory_id)
            .first()
        )
        if model:
            # We can't record movement after delete if cascade delete is on, 
            # but we can record it just before if we want history to persist.
            # However, if cascaded, movements will be gone. 
            # Usually, history should persist even if item is "deleted" (soft delete).
            # If hard delete, history is lost.
            self.session.delete(model)
            self.session.commit()

    def record_movement(self, inventory_id: UUID, movement_type: str, quantity: int, stock_before: int, stock_after: int, reason: str = None, notes: str = None) -> None:
        from src.features.inventory.infrastructure.models.inventory_model import InventoryMovementModel
        movement = InventoryMovementModel(
            inventory_id=inventory_id,
            movement_type=movement_type,
            quantity=quantity,
            stock_before=stock_before,
            stock_after=stock_after,
            reason=reason,
            notes=notes
        )
        self.session.add(movement)
        self.session.commit()

    def get_movements(self, inventory_id: UUID) -> List[dict]:
        from src.features.inventory.infrastructure.models.inventory_model import InventoryMovementModel
        from sqlalchemy import desc
        models = (
            self.session.query(InventoryMovementModel)
            .filter(InventoryMovementModel.inventory_id == inventory_id)
            .order_by(desc(InventoryMovementModel.date))
            .all()
        )
        return [
            {
                "id": str(m.id),
                "movement_type": m.movement_type,
                "quantity": m.quantity,
                "stock_before": m.stock_before,
                "stock_after": m.stock_after,
                "reason": m.reason,
                "notes": m.notes,
                "date": m.date.isoformat()
            }
            for m in models
        ]
