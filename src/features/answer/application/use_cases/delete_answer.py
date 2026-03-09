from uuid import UUID
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository

class DeleteAnswer:
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository

    def execute(self, answer_id: UUID) -> bool:
        return self.answer_repository.delete(answer_id)
