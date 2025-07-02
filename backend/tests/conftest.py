import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    # use in-memory sqlite
    engine = create_engine("sqlite:///:memory:", connect_args={
        "check_same_thread": False})
    connection = engine.connect()

    TestingSessionLocal = sessionmaker(
        bind=connection, autoflush=False, autocommit=False)

    # create tables before tests run
    Base.metadata.create_all(bind=connection)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
