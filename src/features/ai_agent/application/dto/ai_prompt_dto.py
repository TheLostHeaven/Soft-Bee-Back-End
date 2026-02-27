from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID

class AIPromptDTO(BaseModel):
    prompt: str
    session_id: Optional[UUID] = None  # Si se pasa, continúa el contexto
    agent_id: str = "general"        # "experto_apiarios", "soporte", etc.
    provider: str = "mock"           # "openai", "anthropic", "mock"
    context: Optional[Dict[str, Any]] = None
    close_session: bool = False       # Si es True, finaliza y limpia el contexto

    class Config:
        from_attributes = True
