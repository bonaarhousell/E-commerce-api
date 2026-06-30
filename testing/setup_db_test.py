from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()

TEST_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_TEST_NAME")
)

test_engine = create_engine(TEST_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()