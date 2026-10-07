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
    with TestClient(app) as api_client:
        yield api_client


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
        "price": None,
        "quantity": 1,
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


def test_quantity_is_returned_by_create_get_and_list(client: TestClient) -> None:
    created = client.post("/items", json={"name": "Batch", "quantity": 25})
    assert created.status_code == 201
    assert created.json()["quantity"] == 25
    assert client.get("/items/1").json()["quantity"] == 25
    assert client.get("/items").json()[0]["quantity"] == 25


@pytest.mark.parametrize("quantity", [0, 101])
def test_quantity_outside_range_is_rejected(client: TestClient, quantity: int) -> None:
    assert client.post("/items", json={"name": "Batch", "quantity": quantity}).status_code == 422


def test_description_accepts_800_characters_but_rejects_801(client: TestClient) -> None:
    accepted = client.post("/items", json={"name": "Long", "description": "x" * 800})
    assert accepted.status_code == 201
    assert len(accepted.json()["description"]) == 800
    assert client.post("/items", json={"name": "Long", "description": "x" * 801}).status_code == 422
