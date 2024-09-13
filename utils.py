from database import Base
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime

from datetime import datetime
class UrlCreate(BaseModel):
    url: str


class URL_Shorten(Base):
    __tablename__ = 'url_shorten'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255))
    shortCode: Mapped[str] = mapped_column(String(255))
    createdAt: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updatedAt: Mapped[DateTime] = mapped_column(DateTime, onupdate=datetime.now, nullable=True)