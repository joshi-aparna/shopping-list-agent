from datetime import datetime
from getpass import getuser
import subprocess
from zoneinfo import ZoneInfo
from notion_client import Client

from .models import ShoppingItem, ShoppingItems

def get_notion_api_key() -> str:
    result = subprocess.run(
        [
            "security", "find-generic-password",
            "-a", getuser(),
            "-s", "shopping-agent-notion",
            "-w",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def to_notion_properties(item: ShoppingItem) -> dict:
    properties = {
        "Item": {
            "title": [{"text": {"content": item.item}}]
        },
        "Purchased": {"checkbox": item.purchased},
        "Date": {
            "date": {
                "start": (
                    item.date.isoformat()
                    if item.date
                    else datetime.now(
                        ZoneInfo("Asia/Kolkata")
                    ).date().isoformat()
                )
            }
        },
    }

    if item.quantity is not None:
        properties["Quantity"] = {"number": item.quantity}

    if item.unit is not None:
        properties["Unit"] = {"select": {"name": item.unit}}

    if item.category is not None:
        properties["Category"] = {"select": {"name": item.category}}

    return properties

def get_notion_client() -> Client:
    return Client(auth=get_notion_api_key())

def add_shopping_items(
    data_source_id: str,
    shopping_items: ShoppingItems,
) -> list[dict]:
    created_pages = []
    client = Client(auth=get_notion_api_key())
    for item in shopping_items.items:
        page = client.pages.create(
            parent={
                "type": "data_source_id",
                "data_source_id": data_source_id,
            },
            properties=to_notion_properties(item),
        )
        created_pages.append(page)

    return created_pages