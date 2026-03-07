from uuid import UUID
from typing import Optional
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import HiveQuestionDto, UpdateHiveQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class UpdateHiveQuestion:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_question_id: UUID, update_dto: UpdateHiveQuestionDto) -> Optional[HiveQuestionDto]:
        entity = self.question_repository.get_hive_question_by_id(hive_question_id)
        if not entity:
            return None
            
        if update_dto.is_active is not None:
            entity.is_active = update_dto.is_active
        if update_dto.display_order is not None:
            entity.display_order = update_dto.display_order
            
        updated_entity = self.question_repository.update_hive_question(entity)
        return QuestionMapper.hive_to_dto(updated_entity)
