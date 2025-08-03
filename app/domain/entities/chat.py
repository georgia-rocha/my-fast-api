from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    id: int | None
    user_id: int
    """ role: str """
    content: str
    created_at: datetime | None
