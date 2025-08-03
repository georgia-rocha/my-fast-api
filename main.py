from fastapi import FastAPI
from app.adapters.api.user_routes import router as user_router
from app.infrastructure.database import Base, engine
import app.models.chat
import app.models.user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chat API - Hexagonal Architecture")

app.include_router(user_router)
