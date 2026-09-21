from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker,DeclarativeBase
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Generator

class Settings(BaseSettings):
    DATABASE_URL:str
    APP_HOST:str="127.0.0.1"
    APP_PORT:int=8000


    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
        )

settings=Settings()


engine=create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800
)

print("Database Connected Succefully")
SessionLocal=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

#New request scoped DB session Dependency for FastAPI

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:                    # <-- colon here
        db.close()