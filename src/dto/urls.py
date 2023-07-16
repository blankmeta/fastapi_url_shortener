from datetime import datetime

from pydantic import BaseModel


class CreateShortenUrl(BaseModel):
    url: str


class BulkCreateShortenUrl(BaseModel):
    __root__: list[CreateShortenUrl]


class UrlModel(BaseModel):
    url: str
    hashed_url: str

    class Config:
        orm_mode = True


class BulkCreateShortenUrlResponseModel(BaseModel):
    __root__: list[UrlModel]


class StatisticsModel(BaseModel):
    url_id: int
    ip: str


class StatisticsResponseModel(BaseModel):
    id: int
    redirect_datetime: datetime
    ip: str
    url_id: int
