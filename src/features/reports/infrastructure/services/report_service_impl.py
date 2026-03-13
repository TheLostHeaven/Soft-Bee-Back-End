from datetime import datetime
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from src.features.reports.domain.services.report_service import IReportService
from src.features.reports.domain.entities.apiary_report import (
    ApiaryReport,
    ApiaryInfo,
    BeehiveInfo,
    InventoryInfo,
    QuestionAnswerInfo,
    BeehiveDetailReport
)
from src.features.apiaries.infrastructure.models.apiary_model import ApiaryModel
from src.features.beehive.infrastructure.models.beehive_model import BeehiveModel
from src.features.inventory.infrastructure.models.inventory_model import InventoryModel
from src.features.questions.infrastructure.models.question_models import HiveQuestionModel, ApiaryQuestionModel
from src.features.answer.infrastructure.models.answer_models import HiveAnswerModel


class ReportServiceImpl(IReportService):
    """Implementación del servicio de reportes"""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def generate_apiary_report(self, apiary_id: UUID) -> ApiaryReport:
        """Genera un reporte completo del apiario"""
        
        # Obtener información del apiario
        apiary_model = self.db_session.query(ApiaryModel).filter(
            ApiaryModel.id == apiary_id
        ).first()
        
        if not apiary_model:
            raise ValueError(f"Apiario con ID {apiary_id} no encontrado")
        
        apiary_info = ApiaryInfo(
            id=apiary_model.id,
            user_id=apiary_model.user_id,
            name=apiary_model.name,
            location=apiary_model.location,
            beehives_count=apiary_model.beehives_count,
            created_at=apiary_model.created_at,
            updated_at=apiary_model.updated_at
        )
        
        # Obtener inventario
        inventory_models = self.db_session.query(InventoryModel).filter(
            InventoryModel.apiary_id == apiary_id
        ).all()
        
        inventory_list = [
            InventoryInfo(
                id=inv.id,
                name=inv.name,
                quantity=inv.quantity,
                unit=inv.unit,
                description=inv.description,
                minimum_stock=inv.minimum_stock,
                created_at=inv.created_at,
                updated_at=inv.updated_at
            )
            for inv in inventory_models
        ]
        
        # Obtener colmenas con sus preguntas y respuestas
        beehive_models = self.db_session.query(BeehiveModel).filter(
            BeehiveModel.apiary_id == apiary_id
        ).all()
        
        beehive_reports = []
        total_questions = 0
        total_answers = 0
        
        for beehive_model in beehive_models:
            beehive_info = BeehiveInfo(
                id=beehive_model.id,
                hive_number=beehive_model.hive_number,
                activity_level=beehive_model.activity_level,
                bee_population=beehive_model.bee_population,
                food_frames=beehive_model.food_frames,
                brood_frames=beehive_model.brood_frames,
                hive_status=beehive_model.hive_status,
                health_status=beehive_model.health_status,
                has_production_chamber=beehive_model.has_production_chamber,
                observations=beehive_model.observations,
                treatments=beehive_model.treatments,
                created_at=beehive_model.created_at,
                updated_at=beehive_model.updated_at
            )
            
            # Obtener preguntas y respuestas de la colmena
            questions_answers = self._get_beehive_questions_answers(beehive_model.id)
            total_questions += len(questions_answers)
            total_answers += sum(1 for qa in questions_answers if qa.answer is not None)
            
            beehive_reports.append(
                BeehiveDetailReport(
                    beehive=beehive_info,
                    questions_answers=questions_answers
                )
            )
        
        return ApiaryReport(
            apiary=apiary_info,
            inventory=inventory_list,
            beehives=beehive_reports,
            total_questions=total_questions,
            total_answers=total_answers,
            generated_at=datetime.utcnow()
        )

    def _get_beehive_questions_answers(self, hive_id: UUID) -> List[QuestionAnswerInfo]:
        """Obtiene las preguntas y respuestas de una colmena"""
        
        # Query para obtener preguntas de la colmena con sus respuestas
        hive_questions = self.db_session.query(
            HiveQuestionModel,
            ApiaryQuestionModel,
            HiveAnswerModel
        ).join(
            ApiaryQuestionModel,
            HiveQuestionModel.apiary_question_id == ApiaryQuestionModel.id
        ).outerjoin(
            HiveAnswerModel,
            HiveAnswerModel.hive_question_id == HiveQuestionModel.id
        ).filter(
            HiveQuestionModel.hive_id == hive_id,
            HiveQuestionModel.is_active == True
        ).order_by(
            HiveQuestionModel.display_order
        ).all()
        
        questions_answers = []
        for hive_q, apiary_q, answer in hive_questions:
            questions_answers.append(
                QuestionAnswerInfo(
                    question_id=apiary_q.question_id,
                    category=apiary_q.category,
                    question=apiary_q.question,
                    answer=answer.answer if answer else None,
                    score=answer.score if answer else 0,
                    answered_at=answer.answered_at if answer else None
                )
            )
        
        return questions_answers
