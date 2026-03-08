from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from src.features.ai_agent.domain.entities.session import Message

class IAIService(ABC):
    @abstractmethod
    def ask(self, prompt: str, history: List[Message], agent_id: str, provider: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Envia un prompt al agente de IA con su historial y devuelve la respuesta"""
        pass
