from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.db_connection import get_db
from app.main import app
from ....conftest import override_db_conn

app.dependency_overrides[get_db] = override_db_conn


def test_home(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/home")
    response = r.json()
    assert response == "Hello world!"
