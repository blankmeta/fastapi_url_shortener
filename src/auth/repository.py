from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dto import UserDTO
from auth.models import User
from services.base import RepositoryDB, CreateSchemaType, ModelType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RepositoryUser(RepositoryDB[User, UserDTO, UserDTO]):
    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

    async def create(self, db: AsyncSession, *,
                     obj_in: CreateSchemaType) -> ModelType:
        obj_in.password = self.get_password_hash(obj_in.password)
        return await super().create(db, obj_in=obj_in)

    async def get_by_username(
            self, db: AsyncSession, username: str) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.username == username)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()


user_crud = RepositoryUser(User)
