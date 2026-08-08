from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from src.features.statistics.domain.services.statistics_repository import StatisticsRepository
from src.features.statistics.domain.entities.statistics import (
    ApiaryStatistics,
    BeehiveHealthTrend,
    TreatmentDistribution,
    InventoryLevel,
    AnswerScoreTrend
)

class StatisticsRepositoryImpl(StatisticsRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_apiary_statistics(self, apiary_id: UUID) -> Optional[ApiaryStatistics]:
        """Obtiene estadísticas generales de un apiario"""
        from src.features.beehive.infrastructure.models.beehive_model import BeehiveModel
        from src.features.treatments.infrastructure.models.treatment_model import TreatmentModel
        from src.features.inventory.infrastructure.models.inventory_model import InventoryModel
        from src.features.answer.infrastructure.models.answer_models import HiveAnswerModel
        from src.features.questions.infrastructure.models.question_models import HiveQuestionModel
        
        # Total de colmenas
        total_beehives = self.db.query(func.count(BeehiveModel.id))\
            .filter(BeehiveModel.apiary_id == apiary_id).scalar() or 0
        
        # Tratamientos activos
        active_treatments = self.db.query(func.count(TreatmentModel.id))\
            .join(BeehiveModel, TreatmentModel.hive_id == BeehiveModel.id)\
            .filter(
                BeehiveModel.apiary_id == apiary_id,
                TreatmentModel.status == 'active'
            ).scalar() or 0
        
        # Score promedio de salud (basado en respuestas recientes)
        avg_score_result = self.db.query(func.avg(HiveAnswerModel.score))\
            .join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
            .join(BeehiveModel, HiveQuestionModel.hive_id == BeehiveModel.id)\
            .filter(BeehiveModel.apiary_id == apiary_id)\
            .scalar()
        avg_health_score = float(avg_score_result) if avg_score_result else 0.0
        
        # Total de items de inventario
        total_inventory = self.db.query(func.count(InventoryModel.id))\
            .filter(InventoryModel.apiary_id == apiary_id).scalar() or 0
        
        # Items con stock bajo
        low_stock = self.db.query(func.count(InventoryModel.id))\
            .filter(
                InventoryModel.apiary_id == apiary_id,
                InventoryModel.quantity <= InventoryModel.minimum_stock
            ).scalar() or 0
        
        return ApiaryStatistics(
            apiary_id=apiary_id,
            total_beehives=total_beehives,
            active_treatments=active_treatments,
            avg_health_score=round(avg_health_score, 2),
            total_inventory_items=total_inventory,
            low_stock_items=low_stock,
            last_updated=datetime.utcnow()
        )
    
    def get_beehive_health_trends(
        self, 
        apiary_id: UUID, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[BeehiveHealthTrend]:
        """Obtiene tendencias de salud de colmenas"""
        from src.features.beehive.infrastructure.models.beehive_model import BeehiveModel
        from src.features.answer.infrastructure.models.answer_models import HiveAnswerModel
        from src.features.questions.infrastructure.models.question_models import HiveQuestionModel
        
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Obtener colmenas del apiario
        beehives = self.db.query(BeehiveModel)\
            .filter(BeehiveModel.apiary_id == apiary_id)\
            .all()
        
        trends = []
        for hive in beehives:
            # Obtener respuestas en el rango de fechas
            answers = self.db.query(
                func.date(HiveAnswerModel.answered_at).label('date'),
                func.avg(HiveAnswerModel.score).label('avg_score'),
                func.count(HiveAnswerModel.id).label('count')
            ).join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
            .filter(
                HiveQuestionModel.hive_id == hive.id,
                HiveAnswerModel.answered_at.between(start_date, end_date)
            ).group_by(func.date(HiveAnswerModel.answered_at))\
            .order_by(func.date(HiveAnswerModel.answered_at))\
            .all()
            
            data_points = [
                {
                    'date': str(answer.date),
                    'score': round(float(answer.avg_score), 2),
                    'count': answer.count,
                    'status': hive.health_status
                }
                for answer in answers
            ]
            
            if data_points:
                trends.append(BeehiveHealthTrend(
                    hive_id=hive.id,
                    hive_number=hive.hive_number,
                    data_points=data_points
                ))
        
        return trends

    
    def get_treatment_distribution(self, apiary_id: UUID) -> List[TreatmentDistribution]:
        """Obtiene distribución de tratamientos"""
        from src.features.beehive.infrastructure.models.beehive_model import BeehiveModel
        from src.features.treatments.infrastructure.models.treatment_model import TreatmentModel
        
        results = self.db.query(
            TreatmentModel.treatment_type,
            func.count(TreatmentModel.id).label('count')
        ).join(BeehiveModel, TreatmentModel.hive_id == BeehiveModel.id)\
        .filter(BeehiveModel.apiary_id == apiary_id)\
        .group_by(TreatmentModel.treatment_type)\
        .all()
        
        total = sum(r.count for r in results)
        
        return [
            TreatmentDistribution(
                treatment_type=r.treatment_type,
                count=r.count,
                percentage=round((r.count / total * 100), 2) if total > 0 else 0
            )
            for r in results
        ]
    
    def get_inventory_levels(self, apiary_id: UUID) -> List[InventoryLevel]:
        """Obtiene niveles de inventario"""
        from src.features.inventory.infrastructure.models.inventory_model import InventoryModel
        
        items = self.db.query(InventoryModel)\
            .filter(InventoryModel.apiary_id == apiary_id)\
            .all()
        
        levels = []
        for item in items:
            if item.quantity == 0:
                status = 'critical'
            elif item.quantity <= item.minimum_stock:
                status = 'low'
            else:
                status = 'ok'
            
            levels.append(InventoryLevel(
                item_name=item.name,
                current_quantity=item.quantity,
                minimum_stock=item.minimum_stock,
                status=status
            ))
        
        return levels
    
    def get_answer_score_trends(
        self,
        apiary_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AnswerScoreTrend]:
        """Obtiene tendencias de scores de respuestas por categoría"""
        from src.features.beehive.infrastructure.models.beehive_model import BeehiveModel
        from src.features.answer.infrastructure.models.answer_models import HiveAnswerModel
        from src.features.questions.infrastructure.models.question_models import HiveQuestionModel, ApiaryQuestionModel
        
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Query agrupado por categoría y fecha
        results = self.db.query(
            ApiaryQuestionModel.category,
            func.date(HiveAnswerModel.answered_at).label('date'),
            func.avg(HiveAnswerModel.score).label('avg_score'),
            func.count(HiveAnswerModel.id).label('count')
        ).join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
        .join(ApiaryQuestionModel, HiveQuestionModel.apiary_question_id == ApiaryQuestionModel.id)\
        .join(BeehiveModel, HiveQuestionModel.hive_id == BeehiveModel.id)\
        .filter(
            BeehiveModel.apiary_id == apiary_id,
            HiveAnswerModel.answered_at.between(start_date, end_date)
        ).group_by(ApiaryQuestionModel.category, func.date(HiveAnswerModel.answered_at))\
        .order_by(ApiaryQuestionModel.category, func.date(HiveAnswerModel.answered_at))\
        .all()
        
        # Agrupar por categoría
        trends_dict = {}
        for result in results:
            if result.category not in trends_dict:
                trends_dict[result.category] = []
            
            trends_dict[result.category].append({
                'date': str(result.date),
                'avg_score': round(float(result.avg_score), 2),
                'count': result.count
            })
        
        return [
            AnswerScoreTrend(category=category, data_points=data_points)
            for category, data_points in trends_dict.items()
        ]
