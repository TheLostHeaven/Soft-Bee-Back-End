from uuid import UUID
from typing import Optional
from src.features.statistics.domain.services.statistics_repository import StatisticsRepository
from src.features.statistics.domain.entities.statistics import ApiaryStatistics

class GetApiaryStatisticsUseCase:
    def __init__(self, repository: StatisticsRepository):
        self.repository = repository
    
    def execute(self, apiary_id: UUID) -> Optional[ApiaryStatistics]:
        """Obtiene estadísticas generales de un apiario"""
        return self.repository.get_apiary_statistics(apiary_id)
