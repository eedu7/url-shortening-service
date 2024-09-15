from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class UrlBase(BaseModel):
    url: HttpUrl

    class Config:
        orm_mode = True


class UrlCreate(UrlBase):
    pass


class UrlUpdate(UrlBase):
    pass


class UrlRead(UrlBase):
    id: int
    short_code: str
    created_at: datetime
    updated_at: datetime


class UrlState(UrlRead):
    access_count: int
