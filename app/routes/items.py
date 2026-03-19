import logging

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["items"])

# In-memory store for demo purposes
_items: dict[str, dict] = {
    "1": {"id": "1", "name": "Item One", "description": "First item"},
    "2": {"id": "2", "name": "Item Two", "description": "Second item"},
}

# Simulated API key for 401 demo
VALID_API_KEY = "devsecops-demo-key"


class ItemCreate(BaseModel):
    name: str
    description: str = ""


class ItemResponse(BaseModel):
    id: str
    name: str
    description: str


@router.get("/items", response_model=list[ItemResponse])
async def list_items():
    logger.info("Listing all items", extra={"item_count": len(_items)})
    return list(_items.values())


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    if item_id not in _items:
        logger.warning("Item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_id]


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate, x_api_key: str | None = Header(default=None)):
    if x_api_key != VALID_API_KEY:
        logger.warning("Unauthorized access attempt", extra={"provided_key": "***"})
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    item_id = str(len(_items) + 1)
    new_item = {"id": item_id, "name": item.name, "description": item.description}
    _items[item_id] = new_item
    logger.info("Item created", extra={"item_id": item_id, "item_name": item.name})
    return new_item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str, x_api_key: str | None = Header(default=None)):
    if x_api_key != VALID_API_KEY:
        logger.warning("Unauthorized delete attempt", extra={"item_id": item_id})
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    if item_id not in _items:
        logger.warning("Delete failed - item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")

    del _items[item_id]
    logger.info("Item deleted", extra={"item_id": item_id})


@router.get("/error")
async def trigger_error():
    """Endpoint to simulate an application error for alert testing."""
    logger.error("Simulated application error for alert testing")
    raise HTTPException(status_code=500, detail="Simulated error")
