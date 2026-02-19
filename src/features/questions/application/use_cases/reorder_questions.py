from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from uuid import UUID
from typing import List

class ReorderQuestionsUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID, new_order: List[UUID]) -> None:
        if len(new_order) != len(set(new_order)):
            raise ValueError("Duplicate question IDs in order list")
        
        current_questions = self.question_repository.get_by_apiary_id(apiary_id, False)
        current_ids = {q.id for q in current_questions}
        
        if not set(new_order).issubset(current_ids):
             raise ValueError("Order list contains IDs that do not belong to this apiary")
        
        self.question_repository.reorder(apiary_id, new_order)
