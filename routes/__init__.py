import contextlib

from fastapi import FastAPI

from db import create_all_tables

from .url import router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="URL Shortening Service",
)
app.include_router(router, prefix="/shorten", tags=["Shorten"])


@app.get(
    "/",
)
async def root():
    return {"message": "URL Shortening Service"}
