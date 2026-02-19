from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.features.questions.domain.entities.question import Question

class QuestionRepository(ABC):
    @abstractmethod
    def get_by_id(self, question_id: UUID) -> Optional[Question]:
        pass

    @abstractmethod
    def get_by_apiary_id(self, apiary_id: UUID, active_only: bool = True) -> List[Question]:
        pass

    @abstractmethod
    def get_by_external_id(self, apiary_id: UUID, external_id: str) -> Optional[Question]:
        pass

    @abstractmethod
    def create(self, question: Question) -> Question:
        pass

    @abstractmethod
    def update(self, question: Question) -> Question:
        pass

    @abstractmethod
    def delete(self, question_id: UUID) -> None:
        pass

    @abstractmethod
    def reorder(self, apiary_id: UUID, new_order: List[UUID]) -> None:
        pass
