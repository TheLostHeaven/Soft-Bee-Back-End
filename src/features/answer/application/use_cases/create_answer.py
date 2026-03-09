from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.domain.entities.answer import HiveAnswer
from src.features.answer.application.dto.answer_dto import HiveAnswerDto
from src.features.answer.application.mappers.answer_mapper import AnswerMapper

class CreateAnswer:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, hive_question_id: UUID, answer: str, score: int = 0, user_id: Optional[UUID] = None) -> HiveAnswerDto:
        answer_entity = HiveAnswer(
            id=uuid4(),
            hive_question_id=hive_question_id,
            answer=answer,
            score=score,
            answered_by=user_id,
            answered_at=datetime.utcnow()
        )
        
        created_answer = self.answer_repository.create(answer_entity)
        
        # Reload with relationships
        answer_with_details = self.answer_repository.get_by_id(created_answer.id)
        
        return AnswerMapper.to_dto(answer_with_details)
