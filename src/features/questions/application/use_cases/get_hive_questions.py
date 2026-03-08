from uuid import UUID
from typing import List
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import HiveQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class GetHiveQuestions:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_id: UUID) -> List[HiveQuestionDto]:
        entities = self.question_repository.get_hive_questions_by_hive_id(hive_id)
        return [QuestionMapper.hive_to_dto(e) for e in entities]
