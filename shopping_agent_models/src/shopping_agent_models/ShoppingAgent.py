from typing import Protocol

from .ShoppingItem import CartAddResult, CartValue, ClearCartResult, ShoppingItems


class ShoppingAgent(Protocol):

    async def cartadd(
        self,
        items: ShoppingItems,
    ) -> list[CartAddResult]:
        ...

    async def view_cart(self) -> ShoppingItems:
        ...

    async def cartvalue(self) -> CartValue:
        ...

    async def clear_cart(self) -> ClearCartResult:
        ...