import os

from dotenv import load_dotenv

load_dotenv()

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    class Config:
        case_sensitive = True


config: Config = Config()

print(config.DATABASE_URL)
