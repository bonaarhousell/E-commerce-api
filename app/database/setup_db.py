from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if database_url:
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )
    engine = create_engine(database_url)
else:
    db_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )
    engine = create_engine(db_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()