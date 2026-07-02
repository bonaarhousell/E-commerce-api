from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")

print("DATABASE_URL exists:", bool(database_url))
print("DATABASE_URL value:", database_url[:30] + "..." if database_url else None)
if database_url:
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