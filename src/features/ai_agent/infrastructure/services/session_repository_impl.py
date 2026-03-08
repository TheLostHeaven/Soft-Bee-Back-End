from typing import Optional, Dict
from uuid import UUID
from src.features.ai_agent.domain.entities.session import ConversationSession
from src.features.ai_agent.domain.services.session_repository import IAISessionRepository

class InMemoryAISessionRepository(IAISessionRepository):
    def __init__(self):
        self._sessions: Dict[UUID, ConversationSession] = {}

    def save(self, session: ConversationSession) -> None:
        self._sessions[session.id] = session

    def get_by_id(self, session_id: UUID) -> Optional[ConversationSession]:
        return self._sessions.get(session_id)

    def delete(self, session_id: UUID) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
