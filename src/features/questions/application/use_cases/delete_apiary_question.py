from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository

class DeleteApiaryQuestion:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, question_id: UUID) -> bool:
        return self.question_repository.delete_apiary_question(question_id)
