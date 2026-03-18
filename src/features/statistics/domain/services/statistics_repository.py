from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from src.features.statistics.domain.entities.statistics import (
    ApiaryStatistics,
    BeehiveHealthTrend,
    TreatmentDistribution,
    InventoryLevel,
    AnswerScoreTrend
)

class StatisticsRepository(ABC):
    """Interface para el repositorio de estadísticas"""
    
    @abstractmethod
    def get_apiary_statistics(self, apiary_id: UUID) -> Optional[ApiaryStatistics]:
        """Obtiene estadísticas generales de un apiario"""
        pass
    
    @abstractmethod
    def get_beehive_health_trends(
        self, 
        apiary_id: UUID, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[BeehiveHealthTrend]:
        """Obtiene tendencias de salud de colmenas"""
        pass
    
    @abstractmethod
    def get_treatment_distribution(self, apiary_id: UUID) -> List[TreatmentDistribution]:
        """Obtiene distribución de tratamientos"""
        pass
    
    @abstractmethod
    def get_inventory_levels(self, apiary_id: UUID) -> List[InventoryLevel]:
        """Obtiene niveles de inventario"""
        pass
    
    @abstractmethod
    def get_answer_score_trends(
        self,
        apiary_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AnswerScoreTrend]:
        """Obtiene tendencias de scores de respuestas por categoría"""
        pass
