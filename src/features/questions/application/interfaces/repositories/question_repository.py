from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.features.questions.domain.entities.question import Question

class QuestionRepository(ABC):
    @abstractmethod
    def get_by_id(self, question_id: UUID) -> Optional[Question]:
        pass

    @abstractmethod
    def get_by_apiary_id(self, apiary_id: UUID) -> List[Question]:
        pass

    @abstractmethod
    def save(self, question: Question) -> Question:
        pass

    @abstractmethod
    def delete(self, question_id: UUID) -> bool:
        pass

    @abstractmethod
    def update_order(self, apiary_id: UUID, order_ids: List[UUID]) -> bool:
        pass
