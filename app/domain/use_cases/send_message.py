from core.entities.chat import ChatMessage
from core.ports.chat_repository import ChatRepository
from datetime import datetime

class SendMessage:
    def __init__(self, chat_repo: ChatRepository, ai_service):
        self.chat_repo = chat_repo
        self.ai_service = ai_service

    def execute(self, user_id: int, content: str) -> str:
        # Salva mensagem do usuário
        self.chat_repo.save_message(ChatMessage(
            id=None, user_id=user_id, role="user", content=content, created_at=datetime.now()
        ))

        # Busca histórico
        history = self.chat_repo.get_history(user_id)
        messages = [{"role": m.role, "content": m.content} for m in history]

        # Chama IA
        reply = self.ai_service.ask(messages)

        # Salva resposta da IA
        self.chat_repo.save_message(ChatMessage(
            id=None, user_id=user_id, role="assistant", content=reply, created_at=datetime.now()
        ))

        return reply
