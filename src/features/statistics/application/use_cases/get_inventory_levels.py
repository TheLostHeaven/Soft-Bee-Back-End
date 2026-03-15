from uuid import UUID
from typing import List
from src.features.statistics.domain.services.statistics_repository import StatisticsRepository
from src.features.statistics.domain.entities.statistics import InventoryLevel

class GetInventoryLevelsUseCase:
    def __init__(self, repository: StatisticsRepository):
        self.repository = repository
    
    def execute(self, apiary_id: UUID) -> List[InventoryLevel]:
        """Obtiene niveles de inventario"""
        return self.repository.get_inventory_levels(apiary_id)
