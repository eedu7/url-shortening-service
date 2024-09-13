import secrets

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db

from utils import UrlCreate, URL_Shorten, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
def read_root():
    return {"message": "URL Shortening Service"}

@app.post("/shorten")
def shorten(url: UrlCreate, db: Session = Depends(get_db)):
    short_url = "".join(secrets.choice(url.url) for _ in range(6))
    model = URL_Shorten(url=url.url, shortCode=short_url)
    db.add(model)
    db.commit()
    return {
        "id": model.id,
        "url": model.url,
        "shortCode": model.shortCode,
        "createdAt": model.createdAt,
        "updatedAt": model.updatedAt
    }



