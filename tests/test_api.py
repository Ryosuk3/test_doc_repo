import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items


@pytest.fixture(autouse=True)
def reset_items() -> None:
    items._items.clear()
    items._next_id = 1


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_item(client: TestClient) -> None:
    created = client.post(
        "/items",
        json={"name": "Demo", "description": "A test item"},
    )

    assert created.status_code == 201
    assert created.json() == {
        "id": 1,
        "name": "Demo",
        "description": "A test item",
    }

    fetched = client.get("/items/1")
    assert fetched.status_code == 200
    assert fetched.json() == created.json()


def test_missing_item_returns_404(client: TestClient) -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_item_name_is_validated(client: TestClient) -> None:
    response = client.post("/items", json={"name": ""})

    assert response.status_code == 422
