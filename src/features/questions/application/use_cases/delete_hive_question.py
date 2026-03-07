from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository

class DeleteHiveQuestion:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_question_id: UUID) -> bool:
        return self.question_repository.delete_hive_question(hive_question_id)
