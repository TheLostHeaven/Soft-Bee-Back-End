from typing import Dict
from src.features.ai_agent.domain.services.ai_service import IAIService

class AIProviderRegistry:
    def __init__(self, providers: Dict[str, IAIService], default_provider: str = "mock"):
        self._providers = providers
        self._default = default_provider

    def get_provider(self, name: str) -> IAIService:
        return self._providers.get(name, self._providers.get(self._default))
