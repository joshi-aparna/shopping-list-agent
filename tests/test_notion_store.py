from datetime import date

from src.models import ShoppingItem
import os
from dotenv import load_dotenv

from src.models import ShoppingItem, ShoppingItems
from src.notion_store import add_shopping_items, to_notion_properties

load_dotenv()

def test_to_notion_properties():
    item = ShoppingItem(
        item="Rice",
        quantity=2,
        unit="kg",
        category="Groceries",
        date=date(2026, 10, 24),
    )

    properties = to_notion_properties(item)

    assert properties["Item"]["title"][0]["text"]["content"] == "Rice"
    assert properties["Quantity"]["number"] == 2
    assert properties["Unit"]["select"]["name"] == "kg"
    assert properties["Category"]["select"]["name"] == "Groceries"
    assert properties["Purchased"]["checkbox"] is False
    assert properties["Date"]["date"]["start"] == "2026-10-24"

def test_add_shopping_item_to_notion():
    data_source_id = os.environ["NOTION_DATA_SOURCE_ID"]

    items = ShoppingItems(
        items=[ShoppingItem(item="Test Rice", quantity=2, unit="kg")]
    )

    pages = add_shopping_items(data_source_id, items)

    assert len(pages) == 1
    assert pages[0]["id"]