from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.features.statistics.domain.services.statistics_repository import StatisticsRepository
from src.features.statistics.domain.entities.statistics import AnswerScoreTrend

class GetAnswerScoreTrendsUseCase:
    def __init__(self, repository: StatisticsRepository):
        self.repository = repository
    
    def execute(
        self,
        apiary_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AnswerScoreTrend]:
        """Obtiene tendencias de scores de respuestas por categoría"""
        return self.repository.get_answer_score_trends(apiary_id, start_date, end_date)
