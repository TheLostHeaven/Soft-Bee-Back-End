import google.generativeai as genai
from typing import Optional, Dict, Any, List
from src.features.ai_agent.domain.services.ai_service import IAIService
from src.features.ai_agent.domain.entities.session import Message

class GeminiServiceImpl(IAIService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._configured = False
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self._configured = True

    def ask(self, prompt: str, history: List[Message], agent_id: str, provider: str, context: Optional[Dict[str, Any]] = None) -> str:
        if not self._configured:
            return "Error: Gemini API Key no configurada."

        try:
            # Extraer instrucción de sistema si existe
            system_msg = next((m.content for m in history if m.role == 'system'), None)
            
            # Crear modelo con instrucción de sistema
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=system_msg
            )

            # Gemini espera un formato de historial específico
            # roles: 'user', 'model' (en lugar de assistant)
            # Excluimos el mensaje de sistema y el último (prompt actual)
            gemini_history = []
            for msg in history[:-1]:
                if msg.role == 'system':
                    continue
                role = "user" if msg.role == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg.content]})

            # Iniciamos chat con el historial acumulado
            chat = model.start_chat(history=gemini_history)
            
            # Enviamos el prompt actual
            response = chat.send_message(prompt)
            
            return response.text
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error en Gemini: {str(e)}"
