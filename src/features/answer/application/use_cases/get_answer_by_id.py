from uuid import UUID
from typing import Optional
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.application.dto.answer_dto import HiveAnswerDto
from src.features.answer.application.mappers.answer_mapper import AnswerMapper

class GetAnswerById:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, answer_id: UUID) -> Optional[HiveAnswerDto]:
        entity = self.answer_repository.get_by_id(answer_id)
        return AnswerMapper.to_dto(entity) if entity else None
