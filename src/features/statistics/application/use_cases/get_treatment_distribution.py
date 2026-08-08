from uuid import UUID
from typing import List
from src.features.statistics.domain.services.statistics_repository import StatisticsRepository
from src.features.statistics.domain.entities.statistics import TreatmentDistribution

class GetTreatmentDistributionUseCase:
    def __init__(self, repository: StatisticsRepository):
        self.repository = repository
    
    def execute(self, apiary_id: UUID) -> List[TreatmentDistribution]:
        """Obtiene distribución de tratamientos"""
        return self.repository.get_treatment_distribution(apiary_id)
