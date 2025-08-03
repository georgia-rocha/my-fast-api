""" use_case """
from app.domain.ports.user_repository import UserRepository
from app.domain.entities.user import User
from typing import Optional
import bcrypt


class UserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create(self, name: str, email: str, password: str) -> User:
        if self.repo.get_by_email(email):
            raise ValueError("Email already registered")
        hashed_password = self._hash_password(password)
        new_user = User(id=None, name=name, email=email, hashed_password=hashed_password)
        return self.repo.create(new_user)
    
    def get_by_id(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def list_all(self) -> list[User]:
        return self.repo.list_all()

    def update(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> User | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.hashed_password = self._hash_password(password)
        return self.repo.update(user)

    def delete(self, user_id: int) -> bool:
        user = self.repo.get_by_id(user_id)
        if not user:
            return False
        self.repo.delete(user_id)
        return True

    def _hash_password(self, password: str) -> str:
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()