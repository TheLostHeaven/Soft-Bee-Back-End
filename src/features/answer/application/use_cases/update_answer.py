from uuid import UUID
from datetime import datetime
from typing import Optional
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.application.dto.answer_dto import HiveAnswerDto
from src.features.answer.application.mappers.answer_mapper import AnswerMapper

class UpdateAnswer:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, answer_id: UUID, answer: str, score: Optional[int] = None) -> Optional[HiveAnswerDto]:
        existing_answer = self.answer_repository.get_by_id(answer_id)
        
        if not existing_answer:
            return None
        
        existing_answer.answer = answer
        if score is not None:
            existing_answer.score = score
        existing_answer.answered_at = datetime.utcnow()
        
        updated_answer = self.answer_repository.update(existing_answer)
        
        if updated_answer:
            # Reload with relationships
            answer_with_details = self.answer_repository.get_by_id(updated_answer.id)
            return AnswerMapper.to_dto(answer_with_details)
        
        return None
