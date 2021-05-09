import alembic
import pytest

from alembic.config import Config
from fastapi.testclient import TestClient

from main import app


# Apply the database migrations at the beginning and end of the testing session
@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="session")
def db():
    from db.database import get_db

    yield from get_db()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c