from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.features.answer.domain.entities.answer import HiveAnswer

class AnswerRepository(ABC):
    @abstractmethod
    def create(self, answer: HiveAnswer) -> HiveAnswer:
        """Create a new answer"""
        pass

    @abstractmethod
    def create_batch(self, answers: List[HiveAnswer]) -> List[HiveAnswer]:
        """Create multiple answers at once"""
        pass

    @abstractmethod
    def get_by_id(self, answer_id: UUID) -> Optional[HiveAnswer]:
        """Get answer by ID with hive_question details"""
        pass

    @abstractmethod
    def get_by_hive_id(self, hive_id: UUID, limit: Optional[int] = None) -> List[HiveAnswer]:
        """Get all answers for a hive with hive_question details"""
        pass

    @abstractmethod
    def get_latest_by_hive_id(self, hive_id: UUID) -> List[HiveAnswer]:
        """Get the latest answer for each question of a hive"""
        pass

    @abstractmethod
    def get_by_hive_and_question(self, hive_id: UUID, hive_question_id: UUID, limit: Optional[int] = None) -> List[HiveAnswer]:
        """Get all answers for a specific question of a hive (history)"""
        pass

    @abstractmethod
    def get_latest_by_hive_and_question(self, hive_id: UUID, hive_question_id: UUID) -> Optional[HiveAnswer]:
        """Get the latest answer for a specific question of a hive"""
        pass

    @abstractmethod
    def update(self, answer: HiveAnswer) -> HiveAnswer:
        """Update an answer"""
        pass

    @abstractmethod
    def delete(self, answer_id: UUID) -> bool:
        """Delete an answer"""
        pass
