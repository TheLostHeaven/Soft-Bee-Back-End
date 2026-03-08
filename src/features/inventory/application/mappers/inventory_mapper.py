from src.features.inventory.domain.entities.inventory import Inventory
from src.features.inventory.infrastructure.models.inventory_model import InventoryModel
from src.features.inventory.application.dto.inventory_dto import InventoryDTO


class InventoryMapper:
    @staticmethod
    def to_dto(inventory: Inventory) -> InventoryDTO:
        return InventoryDTO(
            id=inventory.id,
            apiary_id=inventory.apiary_id,
            name=inventory.name,
            quantity=inventory.quantity,
            unit=inventory.unit,
            description=inventory.description,
            minimum_stock=inventory.minimum_stock,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )

    @staticmethod
    def to_entity(inventory_model: InventoryModel) -> Inventory:
        return Inventory(
            id=inventory_model.id,
            apiary_id=inventory_model.apiary_id,
            name=inventory_model.name,
            quantity=inventory_model.quantity,
            unit=inventory_model.unit,
            description=inventory_model.description,
            minimum_stock=inventory_model.minimum_stock,
            created_at=inventory_model.created_at,
            updated_at=inventory_model.updated_at,
        )

    @staticmethod
    def to_model(inventory: Inventory) -> InventoryModel:
        return InventoryModel(
            id=inventory.id,
            apiary_id=inventory.apiary_id,
            name=inventory.name,
            quantity=inventory.quantity,
            unit=inventory.unit,
            description=inventory.description,
            minimum_stock=inventory.minimum_stock,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )
