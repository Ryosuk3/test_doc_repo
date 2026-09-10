from fastapi import APIRouter, HTTPException, status

from app.models import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

# Deliberately simple in-memory storage for tests and experiments.
_items: dict[int, Item] = {}
_next_id = 1


@router.get("", response_model=list[Item])
async def list_items() -> list[Item]:
    return list(_items.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate) -> Item:
    global _next_id

    item = Item(id=_next_id, **payload.model_dump())
    _items[item.id] = item
    _next_id += 1
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int) -> None:
    if _items.pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Item not found")
