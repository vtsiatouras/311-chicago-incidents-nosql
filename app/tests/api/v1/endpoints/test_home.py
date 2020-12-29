from fastapi.testclient import TestClient

from app.core.config import settings


def test_home(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/home")
    response = r.json()
    assert response == "Hello world!"
