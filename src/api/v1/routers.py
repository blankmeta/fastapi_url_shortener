from typing import Any, Optional, Union

from fastapi import APIRouter, Depends, status, Query, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse, JSONResponse

from db.db import get_session
from dto.urls import (CreateShortenUrl, StatisticsModel,
                      StatisticsResponseModel, BulkCreateShortenUrl,
                      BulkCreateShortenUrlResponseModel)
from services.url import url_crud, statistics_crud

router = APIRouter()


@router.get('/ping')
async def ping_db(
        db: AsyncSession = Depends(get_session)
) -> Any:
    try:
        statement = select(1)
        await db.execute(statement)
        return JSONResponse(status_code=200, content={
            'db_status': 'up'
        })
    except ConnectionRefusedError:
        return JSONResponse(status_code=500, content={
            'db_status': 'down',
        })


@router.post("/", status_code=status.HTTP_201_CREATED)
async def shorten_url(
        url: CreateShortenUrl,
        db: AsyncSession = Depends(get_session)
):
    """
    Create a shortened url.
    """
    try:
        entity = await url_crud.create(db=db, obj_in=url)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Url already exist")
    return entity


@router.post("/shorten", status_code=status.HTTP_201_CREATED, )
async def multiple_shorten_url(
        urls: BulkCreateShortenUrl,
        db: AsyncSession = Depends(get_session)
) -> BulkCreateShortenUrlResponseModel:
    entities = await url_crud.bulk_create(db=db,
                                          obj_in=urls)
    return entities


@router.post("/{short_url}/delete")
async def set_deleted(
        short_url: str,
        db: AsyncSession = Depends(get_session)
):
    await url_crud.set_deleted(db=db, short_url=short_url)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'deleted'
    })


@router.get("/{short_url}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_original_url(
        short_url: str,
        request: Request,
        db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Redirect to original url by its hash.
    """
    url = await url_crud.get_by_short_url(db=db, short_url=short_url)
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Not found'
        )
    if url.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE
        )

    stats = StatisticsModel(url_id=url.id, ip=request.client.host)
    await statistics_crud.create(db=db, obj_in=stats)

    return RedirectResponse(url.url,
                            status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get("/{short_url}/status")
async def get_status(
        short_url: str,
        full_info: Optional[bool] = None,
        limit: int = Query(alias='max-result', default=10),
        offset: int = Query(default=0),
        db: AsyncSession = Depends(get_session),
) -> Union[StatisticsResponseModel, Any]:
    """
    Get status of url.
    """

    if full_info:
        return await statistics_crud.get_by_short_url(db=db,
                                                      short_url=short_url,
                                                      offset=offset,
                                                      limit=limit)
    count = await statistics_crud.get_count_by_short_url(db=db,
                                                         short_url=short_url)
    return JSONResponse(content={'statistics_count': count}, status_code=200)
