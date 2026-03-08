from openai import OpenAI
from typing import Optional, Dict, Any, List
from src.features.ai_agent.domain.services.ai_service import IAIService
from src.features.ai_agent.domain.entities.session import Message

class OpenAIServiceImpl(IAIService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Inicializamos el cliente oficial
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def ask(self, prompt: str, history: List[Message], agent_id: str, provider: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.client:
            return "Error: OpenAI API Key no configurada correctamente."

        try:
            # Convertimos nuestro historial al formato de OpenAI
            messages = []
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})

            # Llamada usando el SDK oficial
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en el SDK de OpenAI: {str(e)}"
