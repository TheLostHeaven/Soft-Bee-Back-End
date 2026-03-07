from src.features.inventory.application.dto.inventory_dto import CreateInventoryDTO
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.inventory.domain.entities.inventory import Inventory


class CreateInventoryUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, dto: CreateInventoryDTO) -> Inventory:
        inventory = Inventory(
            id=None,
            apiary_id=dto.apiary_id,
            name=dto.name,
            category=dto.category,
            quantity=dto.quantity,
            unit=dto.unit,
            description=dto.description,
            minimum_stock=dto.minimum_stock,
            batch_number=dto.batch_number,
            expiry_date=dto.expiry_date,
            purchase_date=dto.purchase_date,
            supplier=dto.supplier,
            storage_location=dto.storage_location,
            created_at=None,
            updated_at=None,
        )
        return self.repository.create(inventory)
