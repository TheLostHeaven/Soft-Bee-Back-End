from typing import Optional, Dict, Any, List
from src.features.ai_agent.domain.services.ai_service import IAIService
from src.features.ai_agent.domain.entities.session import Message

class MockAIServiceImpl(IAIService):
    def ask(self, prompt: str, history: List[Message], agent_id: str, provider: str, context: Optional[Dict[str, Any]] = None) -> str:
        # Esto es un simulador que conoce el historial
        history_len = len(history)
        context_str = f" con contexto {context}" if context else ""
        
        # Simular que el agente sabe quién es
        agent_role = f"Actuando como Agente: {agent_id} vía {provider}. "
        
        return f"{agent_role}Respuesta simulada para: '{prompt}'. Historial tiene {history_len} mensajes.{context_str}."
