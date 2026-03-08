import google.generativeai as genai
from typing import Optional, Dict, Any, List
from src.features.ai_agent.domain.services.ai_service import IAIService
from src.features.ai_agent.domain.entities.session import Message

class GeminiServiceImpl(IAIService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            self.model = None

    def ask(self, prompt: str, history: List[Message], agent_id: str, provider: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self.model:
            return "Error: Gemini API Key no configurada."

        try:
            # Gemini espera un formato de historial específico
            # roles: 'user', 'model' (en lugar de assistant)
            gemini_history = []
            for msg in history[:-1]: # Tomamos todo menos el último mensaje (que es el prompt actual)
                role = "user" if msg.role == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg.content]})

            # Iniciamos chat con el historial acumulado
            chat = self.model.start_chat(history=gemini_history)
            
            # Enviamos el prompt actual
            response = chat.send_message(prompt)
            
            return response.text
        except Exception as e:
            return f"Error en Gemini: {str(e)}"
