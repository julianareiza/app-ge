import os

import pytest
from httpx import ASGITransport, AsyncClient

os.environ["OTEL_ENABLED"] = "false"

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_list_items():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_get_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"


@pytest.mark.anyio
async def test_get_item_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/items/999")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_item_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/items",
            json={"name": "Test", "description": "Test item"},
        )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_create_item_authorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/items",
            json={"name": "Test", "description": "Test item"},
            headers={"x-api-key": "devsecops-demo-key"},
        )
    assert response.status_code == 201
    assert response.json()["name"] == "Test"
