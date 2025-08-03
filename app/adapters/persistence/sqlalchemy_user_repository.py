""" persistence/sqlalchemy_user_repository.py """

from app.domain.ports.user_repository import UserRepository
from app.domain.entities.user import User  # entidade de domínio
from app.infrastructure.database import SessionLocal
from app.models.user import User as UserModel  # model do banco
from pydantic import BaseModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db=None):
        self.db = db or SessionLocal()

    def create(self, user: User) -> User:
        db_user = UserModel(name=user.name, email=user.email, hashed_password=user.hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User(id=db_user.id, name=db_user.name, email=db_user.email, hashed_password=db_user.hashed_password)
    

    def get_by_id(self, user_id: int) -> User | None:
            db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if not db_user:
                return None
            return User(id=db_user.id, name=db_user.name, email=db_user.email, hashed_password=db_user.hashed_password)

    def get_by_email(self, email: str) -> User | None:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None
        return User(id=db_user.id, name=db_user.name, email=db_user.email, hashed_password=db_user.hashed_password)

    def list_all(self) -> list[User]:
        return [
            User(id=u.id, name=u.name, email=u.email, hashed_password=u.hashed_password)
            for u in self.db.query(UserModel).all()
        ]

    def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            return None
        db_user.name = user.name
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password  # Certifique-se de que a senha está sendo atualizada
        self.db.commit()
        self.db.refresh(db_user)
        return User(id=db_user.id, name=db_user.name, email=db_user.email, hashed_password=db_user.hashed_password)

    def delete(self, user_id: int) -> None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
