from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import QuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper
from uuid import UUID
from typing import List

class GetApiaryQuestionsUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID, active_only: bool = True) -> List[QuestionDto]:
        entities = self.question_repository.get_by_apiary_id(apiary_id, active_only)
        return [QuestionMapper.to_dto(entity) for entity in entities]
