from abc import ABC, abstractmethod
from app.domain.entities.chat import ChatMessage

class ChatRepository(ABC):
    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        pass

    @abstractmethod
    def get_history(self, user_id: int) -> list[ChatMessage]:
        pass
