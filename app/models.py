from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    # Validation is shared by create requests and stored item responses.
    price: float | None = Field(default=None, ge=0)
    quantity: int = Field(default=1, ge=1, le=100)
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=800)


class Item(ItemCreate):
    id: int
