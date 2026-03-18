from uuid import uuid4, UUID
from typing import List
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import HiveQuestion
from src.features.questions.application.dto.question_dto import HiveQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class InitializeHiveQuestions:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_id: UUID, apiary_id: UUID) -> List[HiveQuestionDto]:
        # 1. Obtener preguntas actuales de la colmena (si existen)
        existing_hqs = self.question_repository.get_hive_questions_by_hive_id(hive_id)
        existing_apiary_q_ids = {hq.apiary_question_id for hq in existing_hqs}

        # 2. Obtener preguntas del apiario
        apiary_questions = self.question_repository.get_apiary_questions_by_apiary_id(apiary_id)
        
        hive_questions_to_create = []
        for aq in apiary_questions:
            # Solo crear si no existe ya para esta colmena
            if aq.id not in existing_apiary_q_ids:
                hq = HiveQuestion(
                    id=uuid4(),
                    hive_id=hive_id,
                    apiary_question_id=aq.id,
                    display_order=aq.display_order,
                    is_active=True
                )
                hive_questions_to_create.append(hq)
            
        if hive_questions_to_create:
            self.question_repository.create_hive_questions_batch(hive_questions_to_create)
            
        # 3. Retornar todas las preguntas (nuevas + existentes)
        final_entities = self.question_repository.get_hive_questions_by_hive_id(hive_id)
        return [QuestionMapper.hive_to_dto(e) for e in final_entities]
