from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.url import UrlCrud
from db import get_async_session
from helpers import short_code
from models.url import URL_Shortener
from schemas import UrlCreate, UrlRead, UrlState, UrlUpdate

router = APIRouter()


@router.get("/{code}/stats", response_model=UrlState)
async def get_stats(code: str, session: AsyncSession = Depends(get_async_session)):
    url_crud = UrlCrud(URL_Shortener, session)
    url = await url_crud.get_by(field="short_code", value=code)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )
    return url


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UrlRead)
async def create_short_code(
    new_url: UrlCreate, session: AsyncSession = Depends(get_async_session)
):
    url_crud = UrlCrud(URL_Shortener, session)
    exist = await url_crud.get_by("url", new_url.url)
    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL already exists",
        )
    try:
        code = short_code(str(new_url.url))
        url = await url_crud.create({"url": str(new_url.url), "short_code": str(code)})
        return url

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating short code: {e}",
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UrlRead])
async def read_short_codes(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)
):
    url_crud = UrlCrud(URL_Shortener, session)
    urls = await url_crud.get_all(skip=skip, limit=limit)
    if urls is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No urls found",
        )
    return urls


@router.get("/{code}", response_model=UrlRead)
async def get_original_url(
    code: str, session: AsyncSession = Depends(get_async_session)
):
    url_crud = UrlCrud(URL_Shortener, session)
    url = await url_crud.get_by("short_code", code)
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No url found",
        )
    await url_crud.update_access_count(code)
    return url


@router.put("/{code}", response_model=UrlRead)
async def update_url(
    code: str, new_url: UrlUpdate, session: AsyncSession = Depends(get_async_session)
):
    url_crud = UrlCrud(URL_Shortener, session)
    url = await url_crud.update(attributes=new_url.model_dump(), code=code)
    return url


@router.delete("/{code}")
async def delete_url(
    code: str, session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    url_crud = UrlCrud(URL_Shortener, session)
    deleted = await url_crud.delete("short_code", code)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No url found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "Url deleted successfully!"}
    )
