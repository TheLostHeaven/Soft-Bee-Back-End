from typing import Dict, Any, Optional
from uuid import UUID

from src.features.ai_agent.infrastructure.services.ai_provider_registry import AIProviderRegistry
from src.features.ai_agent.domain.services.session_repository import IAISessionRepository
from src.features.ai_agent.domain.entities.session import ConversationSession
from src.features.ai_agent.application.dto.ai_prompt_dto import AIPromptDTO

class ProcessAIPromptUseCase:
    def __init__(self, provider_registry: AIProviderRegistry, session_repository: IAISessionRepository):
        self.provider_registry = provider_registry
        self.session_repository = session_repository

    def execute(self, dto: AIPromptDTO) -> Dict[str, Any]:
        # 1. Obtener o crear sesión
        session = self._get_or_create_session(dto.session_id, dto.agent_id)
        
        # 2. Si el usuario pide cerrar, cerramos y limpiamos
        if dto.close_session:
            self.session_repository.delete(session.id)
            return {
                "status": "session_closed",
                "message": "La sesión ha sido finalizada y el contexto limpiado.",
                "session_id": str(session.id)
            }

        # 3. Seleccionar el proveedor (OpenAI, Mock, etc.)
        ai_service = self.provider_registry.get_provider(dto.provider)

        # 4. Añadir el prompt del usuario al historial
        session.add_message("user", dto.prompt)
        
        # 5. Llamar a la IA con todo el historial
        response_content = ai_service.ask(
            dto.prompt, 
            session.history, 
            session.agent_id, 
            dto.provider,
            dto.context
        )
        
        # 6. Añadir respuesta de la IA al historial
        session.add_message("assistant", response_content)
        
        # 7. Guardar sesión actualizada
        self.session_repository.save(session)
        
        return {
            "status": "success",
            "session_id": str(session.id),
            "agent_id": session.agent_id,
            "provider_used": dto.provider,
            "data": {
                "response": response_content,
                "is_finished": False
            }
        }

    def _get_or_create_session(self, session_id: Optional[UUID], agent_id: str) -> ConversationSession:
        if session_id:
            session = self.session_repository.get_by_id(session_id)
            if session and session.is_active:
                return session
        
        # Crear nueva sesión si no existe o no es válida
        new_session = ConversationSession(agent_id=agent_id)
        self.session_repository.save(new_session)
        return new_session
