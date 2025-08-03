""" router """

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.adapters.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.use_cases.user import UserUseCase
from typing import Optional
from pydantic import BaseModel
from app.models.user import User as UserModel
from app.domain.entities.user import User as UserEntity

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

def get_user_use_case(db: Session = Depends(get_db)) -> UserUseCase:
    repo = SQLAlchemyUserRepository(db)
    return UserUseCase(repo)

@router.post("/")
def create_user(user: UserCreateRequest, use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        return use_case.create(user.name, user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
def get_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    user = use_case.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def list_users(use_case: UserUseCase = Depends(get_user_use_case)):
    return use_case.list_all()

@router.put("/{user_id}")
def update_user(user_id: int, update_data: UserUpdateRequest, use_case: UserUseCase = Depends(get_user_use_case)):
    user = use_case.update(user_id, update_data.name, update_data.email, update_data.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    success = use_case.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
    repo = SQLAlchemyUserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    repo.db.delete(repo.db.query(repo.db.query(UserUpdateRequest)).filter_by(id=user_id).first())
    repo.db.commit()

    return {"message": "User deleted successfully"}