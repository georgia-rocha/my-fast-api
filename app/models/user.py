""" model """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    # Lista de mensagens associadas ao usuário
    chat_messages = relationship("ChatMessageModel", back_populates="user")
