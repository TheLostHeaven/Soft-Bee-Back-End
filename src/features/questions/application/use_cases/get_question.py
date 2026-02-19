from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import QuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper
from uuid import UUID
from typing import Optional

class GetQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, question_id: UUID) -> Optional[QuestionDto]:
        entity = self.question_repository.get_by_id(question_id)
        return QuestionMapper.to_dto(entity) if entity else None
