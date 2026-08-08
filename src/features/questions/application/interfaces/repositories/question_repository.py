from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.features.questions.domain.entities.question import ApiaryQuestion, HiveQuestion

class QuestionRepository(ABC):
    # Apiary Questions
    @abstractmethod
    def create_apiary_question(self, question: ApiaryQuestion) -> ApiaryQuestion:
        pass

    @abstractmethod
    def create_apiary_questions_batch(self, questions: List[ApiaryQuestion]) -> List[ApiaryQuestion]:
        pass
    
    @abstractmethod
    def get_apiary_questions_by_apiary_id(self, apiary_id: UUID) -> List[ApiaryQuestion]:
        pass

    @abstractmethod
    def get_apiary_question_by_id(self, apiary_question_id: UUID) -> Optional[ApiaryQuestion]:
        pass

    @abstractmethod
    def update_apiary_question(self, question: ApiaryQuestion) -> ApiaryQuestion:
        pass

    @abstractmethod
    def delete_apiary_question(self, question_id: UUID) -> bool:
        pass

    # Hive Questions
    @abstractmethod
    def create_hive_question(self, question: HiveQuestion) -> HiveQuestion:
        pass

    @abstractmethod
    def create_hive_questions_batch(self, questions: List[HiveQuestion]) -> List[HiveQuestion]:
        pass

    @abstractmethod
    def get_hive_questions_by_hive_id(self, hive_id: UUID) -> List[HiveQuestion]:
        pass

    @abstractmethod
    def update_hive_question(self, question: HiveQuestion) -> HiveQuestion:
        pass

    @abstractmethod
    def delete_hive_question(self, hive_question_id: UUID) -> bool:
        pass
    
    @abstractmethod
    def get_hive_question_by_id(self, hive_question_id: UUID) -> Optional[HiveQuestion]:
        pass
