from uuid import UUID
from typing import List, Optional
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.application.dto.answer_dto import HiveAnswerDto
from src.features.answer.application.mappers.answer_mapper import AnswerMapper

class GetAnswersByHive:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, hive_id: UUID, limit: Optional[int] = None, latest_only: bool = False) -> List[HiveAnswerDto]:
        if latest_only:
            entities = self.answer_repository.get_latest_by_hive_id(hive_id)
        else:
            entities = self.answer_repository.get_by_hive_id(hive_id, limit)
        
        return [AnswerMapper.to_dto(e) for e in entities]
