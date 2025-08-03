from app.domain.ports.chat_repository import ChatRepository
from app.domain.entities.chat import ChatMessage
from app.models.chat import ChatMessageModel
from sqlalchemy.orm import Session

class SQLAlchemyChatRepository(ChatRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        db_msg = ChatMessageModel(
            user_id=message.user_id,
            role=message.role,
            content=message.content
        )
        self.db.add(db_msg)
        self.db.commit()
        self.db.refresh(db_msg)
        return ChatMessage(db_msg.id, db_msg.user_id, db_msg.role, db_msg.content, db_msg.created_at)

    def get_history(self, user_id: int) -> list[ChatMessage]:
        msgs = self.db.query(ChatMessageModel).filter_by(user_id=user_id).order_by(ChatMessageModel.created_at).all()
        return [
            ChatMessage(m.id, m.user_id, m.role, m.content, m.created_at)
            for m in msgs
        ]
