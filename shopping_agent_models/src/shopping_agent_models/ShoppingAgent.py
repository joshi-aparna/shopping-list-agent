from typing import Protocol

from .ShoppingItem import ShoppingListItems


class ShoppingAgent(Protocol):

    async def cartadd(
        self,
        items: ShoppingListItems
    ) -> None:
        ...

    async def view_cart(self):
        ...

    async def cartvalue(self):
        ...

    async def clear_cart(self):
        ...