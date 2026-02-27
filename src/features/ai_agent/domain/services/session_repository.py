from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from src.features.ai_agent.domain.entities.session import ConversationSession

class IAISessionRepository(ABC):
    @abstractmethod
    def save(self, session: ConversationSession) -> None:
        pass

    @abstractmethod
    def get_by_id(self, session_id: UUID) -> Optional[ConversationSession]:
        pass

    @abstractmethod
    def delete(self, session_id: UUID) -> None:
        pass
