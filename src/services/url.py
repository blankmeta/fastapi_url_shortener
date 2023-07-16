import hashlib
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from dto.urls import CreateShortenUrl, StatisticsModel
from models.models import Url, Statistics
from services.base import RepositoryDB, CreateSchemaType, ModelType


class RepositoryUrl(RepositoryDB[Url, CreateShortenUrl, CreateShortenUrl]):

    async def create(self, db: AsyncSession, *,
                     obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(
            **obj_in_data,
            hashed_url=hashlib.md5(
                obj_in_data.get('url').encode('utf8')).hexdigest(),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_short_url(self,
                               db: AsyncSession,
                               short_url: str) -> Optional[ModelType]:
        statement = select(
            self._model
        ).where(
            self._model.hashed_url == short_url
        )
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def bulk_create(self,
                          db: AsyncSession,
                          obj_in: list[CreateSchemaType]):
        obj_in_data = jsonable_encoder(obj_in)
        url_objects = []

        for url in obj_in_data:
            db_obj = self._model(
                **url,
                hashed_url=hashlib.md5(
                    url.get('url').encode('utf8')).hexdigest(),
            )
            db.add(db_obj)
            url_objects.append(db_obj)

        await db.commit()
        for url in url_objects:
            await db.refresh(url)
        return url_objects

    async def set_deleted(self,
                          db: AsyncSession,
                          short_url: str):
        statement = update(
            self._model
        ).where(
            self._model.hashed_url == short_url
        ).values(
            is_deleted=True
        )

        await db.execute(statement=statement)
        await db.commit()


class RepositoryStatistics(RepositoryDB[
                               Statistics, StatisticsModel, StatisticsModel]):
    async def get_by_short_url(self, db: AsyncSession,
                               short_url: str,
                               offset: int,
                               limit: int):
        statement = select(
            self._model
        ).join(Url).where(
            Url.hashed_url == short_url
        ).offset(offset).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def get_count_by_short_url(self, db: AsyncSession,
                                     short_url: str):
        statement = select(
            count()
        ).select_from(self._model).join(Url).where(
            Url.hashed_url == short_url
        )
        result = await db.execute(statement=statement)
        return result.scalar_one_or_none()


url_crud = RepositoryUrl(Url)
statistics_crud = RepositoryStatistics(Statistics)
