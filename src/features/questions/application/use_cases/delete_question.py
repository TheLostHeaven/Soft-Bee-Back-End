from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from uuid import UUID

class DeleteQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, question_id: UUID) -> None:
        self.question_repository.delete(question_id)
