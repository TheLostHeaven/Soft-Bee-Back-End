from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Optional, Dict
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.domain.entities.answer import HiveAnswer
from src.features.answer.application.dto.answer_dto import HiveAnswerDto
from src.features.answer.application.mappers.answer_mapper import AnswerMapper

class CreateAnswersBatch:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, answers_data: List[Dict], user_id: Optional[UUID] = None) -> List[HiveAnswerDto]:
        """
        answers_data: List of dicts with keys: hive_question_id, answer, score (optional)
        """
        answers = []
        answered_at = datetime.utcnow()
        
        for data in answers_data:
            answer = HiveAnswer(
                id=uuid4(),
                hive_question_id=data.get("hive_question_id"),
                answer=data.get("answer"),
                score=data.get("score", 0),
                answered_by=user_id,
                answered_at=answered_at
            )
            answers.append(answer)
        
        created_answers = self.answer_repository.create_batch(answers)
        
        # Reload with relationships
        result = []
        for answer in created_answers:
            answer_with_details = self.answer_repository.get_by_id(answer.id)
            result.append(AnswerMapper.to_dto(answer_with_details))
        
        return result
