import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.api.v1 import events, locations
from app.main import app


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def override_engine(engine, monkeypatch):
    monkeypatch.setattr(events, "engine", engine)
    monkeypatch.setattr(locations, "engine", engine)


@pytest.fixture(name="client")
def client_fixture():
    return TestClient(app)
