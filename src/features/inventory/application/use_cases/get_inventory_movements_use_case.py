from typing import List
from uuid import UUID
from src.features.inventory.application.interfaces.repositories.inventory_repository import InventoryRepository
from src.features.inventory.domain.entities.inventory import InventoryMovement

class GetInventoryMovementsUseCase:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def execute(self, inventory_id: UUID) -> List[InventoryMovement]:
        return self.repository.get_movements(inventory_id)
