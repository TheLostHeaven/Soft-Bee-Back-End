from uuid import UUID
from typing import List
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import ApiaryQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class GetApiaryQuestions:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID) -> List[ApiaryQuestionDto]:
        entities = self.question_repository.get_apiary_questions_by_apiary_id(apiary_id)
        return [QuestionMapper.apiary_to_dto(e) for e in entities]
