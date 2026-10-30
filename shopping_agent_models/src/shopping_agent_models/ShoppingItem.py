from __future__ import annotations
from datetime import date as Date

from pydantic import BaseModel, Field


class ShoppingItem(BaseModel):
    item: str = Field(description="Name of the item")
    quantity: float | None = None
    unit: str | None = None
    category: str | None = None
    purchased: bool = False
    date: Date | None = None

class ShoppingItems(BaseModel):
    items: list[ShoppingItem]