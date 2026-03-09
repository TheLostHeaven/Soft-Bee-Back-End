from uuid import UUID
from typing import List, Optional
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.application.dto.answer_dto import HiveAnswerDto
from src.features.answer.application.mappers.answer_mapper import AnswerMapper

class GetAnswerHistory:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, hive_id: UUID, hive_question_id: UUID, limit: Optional[int] = None) -> List[HiveAnswerDto]:
        """Get the history of answers for a specific question"""
        entities = self.answer_repository.get_by_hive_and_question(hive_id, hive_question_id, limit)
        return [AnswerMapper.to_dto(e) for e in entities]
