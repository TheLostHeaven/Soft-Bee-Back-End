from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID, uuid4

@dataclass
class Message:
    role: str # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ConversationSession:
    id: UUID = field(default_factory=uuid4)
    agent_id: str = "general"
    history: List[Message] = field(default_factory=list)
    is_active: bool = True
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_message(self, role: str, content: str):
        self.history.append(Message(role=role, content=content))
        self.updated_at = datetime.now()
    
    def close(self):
        self.is_active = False
        self.updated_at = datetime.now()
