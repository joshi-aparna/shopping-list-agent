import os

from dotenv import load_dotenv
from notion_client import Client

from .agent import agent
from .notion_store import add_shopping_items

load_dotenv()


def process_shopping_message(message: str) -> int:
    result = agent.run_sync(message)
    shopping_items = result.output
    if not shopping_items.items:
        return 0
    data_source_id = os.environ["NOTION_DATA_SOURCE_ID"]

    created_pages = add_shopping_items(
        data_source_id,
        shopping_items,
    )

    return len(created_pages)