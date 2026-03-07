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
        # Obtener preguntas del apiario
        apiary_questions = self.question_repository.get_apiary_questions_by_apiary_id(apiary_id)
        
        hive_questions = []
        for aq in apiary_questions:
            hq = HiveQuestion(
                id=uuid4(),
                hive_id=hive_id,
                apiary_question_id=aq.id,
                display_order=aq.display_order,
                is_active=True
            )
            hive_questions.append(hq)
            
        if hive_questions:
            entities = self.question_repository.create_hive_questions_batch(hive_questions)
            return [QuestionMapper.hive_to_dto(e) for e in entities]
        return []
