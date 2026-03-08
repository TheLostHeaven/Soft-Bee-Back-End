from openai import OpenAI
from typing import Optional, Dict, Any, List
from src.features.ai_agent.domain.services.ai_service import IAIService
from src.features.ai_agent.domain.entities.session import Message

class DeepSeekServiceImpl(IAIService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # DeepSeek usa el SDK de OpenAI con una base_url diferente
        self.client = OpenAI(
            api_key=self.api_key, 
            base_url="https://api.deepseek.com"
        ) if self.api_key else None

    def ask(self, prompt: str, history: List[Message], agent_id: str, provider: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.client:
            return "Error: DeepSeek API Key no configurada."

        try:
            messages = []
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})

            completion = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en DeepSeek: {str(e)}"
