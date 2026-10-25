import getpass
import subprocess
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

def test_data_source_access():
    data_source_id = os.environ["NOTION_DATA_SOURCE_ID"]
    result = notion.data_sources.retrieve(
        data_source_id=data_source_id
    )
    assert result["id"] == data_source_id
    print("Data source access verified.")


def get_notion_api_key() -> str:
    result = subprocess.run(
        [
            "security", "find-generic-password",
            "-a", getpass.getuser(),
            "-s", "shopping-agent-notion",
            "-w",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def test_query_shopping_list():
    data_source_id = os.environ["NOTION_DATA_SOURCE_ID"]
    result = notion.data_sources.query(
        data_source_id=data_source_id
    )
    print(f"Found {len(result['results'])} shopping list items.")


notion = Client(auth=get_notion_api_key())

print(notion.users.me())
test_data_source_access()
test_query_shopping_list()