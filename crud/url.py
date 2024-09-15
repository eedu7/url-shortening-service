from typing import Any, Generic, Type, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from models import Base

ModelType = TypeVar("ModelType", bound=Base)


class UrlCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.session = session
        self.model = model

    async def create(self, attributes: dict[str, Any]) -> ModelType:
        if attributes is None:
            attributes = {}

        model = self.model(**attributes)
        self.session.add(model)
        await self.session.commit()
        return model

    async def get_by(self, field: str, value: any) -> ModelType:
        query = select(self.model).where(getattr(self.model, field) == value)
        result = await self.session.scalars(query)
        return result.first()

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def update_access_count(self, code: str):
        url = await self.get_by("short_code", code)
        if url is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Url not found"
            )

        url.access_count += 1
        await self.session.commit()

    async def update(self, attributes: dict[str, Any], code: str) -> ModelType:
        url = await self.get_by(field="short_code", value=code)
        if url is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Url not found"
            )
        for key, value in attributes.items():
            setattr(url, key, value)
            await self.session.commit()

        return url

    async def delete(self, field: str, code: str) -> bool:
        url = await self.get_by(field=field, value=code)
        if url is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Url not found"
            )

        await self.session.delete(url)
        await self.session.commit()
        return True
