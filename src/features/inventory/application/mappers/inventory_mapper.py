from src.features.inventory.domain.entities.inventory import Inventory, InventoryMovement
from src.features.inventory.infrastructure.models.inventory_model import InventoryModel, InventoryMovementModel
from src.features.inventory.application.dto.inventory_dto import InventoryDTO, InventoryMovementDTO


class InventoryMapper:
    @staticmethod
    def to_dto(inventory: Inventory) -> InventoryDTO:
        return InventoryDTO(
            id=inventory.id,
            apiary_id=inventory.apiary_id,
            name=inventory.name,
            category=inventory.category,
            quantity=inventory.quantity,
            unit=inventory.unit,
            description=inventory.description,
            minimum_stock=inventory.minimum_stock,
            batch_number=inventory.batch_number,
            expiry_date=inventory.expiry_date,
            supplier=inventory.supplier,
            storage_location=inventory.storage_location,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )

    @staticmethod
    def to_entity(inventory_model: InventoryModel) -> Inventory:
        return Inventory(
            id=inventory_model.id,
            apiary_id=inventory_model.apiary_id,
            name=inventory_model.name,
            category=inventory_model.category,
            quantity=inventory_model.quantity,
            unit=inventory_model.unit,
            description=inventory_model.description,
            minimum_stock=inventory_model.minimum_stock,
            batch_number=inventory_model.batch_number,
            expiry_date=inventory_model.expiry_date,
            supplier=inventory_model.supplier,
            storage_location=inventory_model.storage_location,
            created_at=inventory_model.created_at,
            updated_at=inventory_model.updated_at,
        )

    @staticmethod
    def to_model(inventory: Inventory) -> InventoryModel:
        return InventoryModel(
            id=inventory.id,
            apiary_id=inventory.apiary_id,
            name=inventory.name,
            category=inventory.category,
            quantity=inventory.quantity,
            unit=inventory.unit,
            description=inventory.description,
            minimum_stock=inventory.minimum_stock,
            batch_number=inventory.batch_number,
            expiry_date=inventory.expiry_date,
            supplier=inventory.supplier,
            storage_location=inventory.storage_location,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )

    @staticmethod
    def movement_to_entity(model: InventoryMovementModel) -> InventoryMovement:
        return InventoryMovement(
            id=model.id,
            inventory_id=model.inventory_id,
            movement_type=model.movement_type,
            quantity=model.quantity,
            stock_before=model.stock_before,
            stock_after=model.stock_after,
            reason=model.reason,
            date=model.date,
            notes=model.notes
        )

    @staticmethod
    def movement_to_dto(entity: InventoryMovement) -> InventoryMovementDTO:
        return InventoryMovementDTO(
            id=entity.id,
            inventory_id=entity.inventory_id,
            movement_type=entity.movement_type,
            quantity=entity.quantity,
            stock_before=entity.stock_before,
            stock_after=entity.stock_after,
            reason=entity.reason,
            date=entity.date,
            notes=entity.notes
        )
