from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.adapters.persistence.sqlalchemy_chat_repository import SQLAlchemyChatRepository
from app.adapters.ai.openai_chat_service import OpenAIChatService
from core.use_cases.send_message import SendMessage
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    content: str

@router.post("/{user_id}")
def send_message(user_id: int, request: ChatRequest, db: Session = Depends(get_db)):
    chat_repo = SQLAlchemyChatRepository(db)
    ai_service = OpenAIChatService()
    use_case = SendMessage(chat_repo, ai_service)
    reply = use_case.execute(user_id, request.content)
    return {"reply": reply}
