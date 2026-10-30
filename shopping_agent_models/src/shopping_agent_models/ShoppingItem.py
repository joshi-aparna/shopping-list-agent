from __future__ import annotations
from datetime import date as Date

from pydantic import BaseModel, Field
from enum import StrEnum

class ShoppingOperation(StrEnum):
    CART_ADD = "cartadd"
    VIEW_CART = "view_cart"
    CART_VALUE = "cartvalue"
    CLEAR_CART = "clear_cart"
    LIST_ADD = "listadd"
    VIEW_LIST = "view_list"

class ShoppingItem(BaseModel):
    item: str = Field(description="Name of the item")
    quantity: float | None = None
    unit: str | None = None
    category: str | None = None
    purchased: bool = False
    date: Date | None = None

class ShoppingItems(BaseModel):
    items: list[ShoppingItem]

class CartAddResult(BaseModel):
    item: str
    success: bool
    message: str

class CartValue(BaseModel):
    total: float
    item_count: int
    message: str

class ClearCartResult(BaseModel):
    success: bool
    items_removed: int
    message: str