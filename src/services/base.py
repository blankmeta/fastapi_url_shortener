from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, \
    Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository:

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository,
                   Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        statement = select(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(
            self, db: AsyncSession, *, skip=0, limit=100
    ) -> Sequence[Any]:
        statement = select(self._model).offset(skip).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(self, db: AsyncSession, *,
                     obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_object: ModelType,
            object_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        obj_in_data = dict(object_in)
        obj_in_data.pop("id", None)
        statement = (
            update(self._model)
            .filter_by(id=db_object.id)
            .values(**obj_in_data)
        )
        await db.execute(statement=statement)
        await db.commit()
        await db.refresh(db_object)
        return db_object

    async def delete(self, db: AsyncSession, *, id: int | None = None) -> None:
        filter = {"id": id} if id else {}
        statement = delete(self._model).filter_by(**filter)
        await db.execute(statement=statement)
        await db.commit()
