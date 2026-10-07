from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    price: float | None = Field(default=None, ge=0)
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class Item(ItemCreate):
    id: int
