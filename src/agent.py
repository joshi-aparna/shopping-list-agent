import os
os.environ["PYDANTIC_AI_NO_BANNER"] = "1"
#import json
#import httpx
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from shopping_agent_models import ShoppingItems

#async def inspect_request(request: httpx.Request) -> None:
#    print("\n--- Actual HTTP request body ---")
#    print(json.dumps(
#        json.loads(request.content),
#        indent=2,
#    ))
#http_client = httpx.AsyncClient(
#   event_hooks={"request": [inspect_request]}
#)

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:30b")

model = OpenAIChatModel(
    MODEL_NAME,
    provider=OpenAIProvider(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
 #       http_client=http_client,
    ),
)

agent = Agent(
    model,
    output_type=ShoppingItems,
    retries=3,
    instructions = (
    "Extract every shopping list item mentioned in the user's message. "
    "Return each item in the 'items' list. "
    "Do not return an empty list if shopping items are mentioned. "
    "Preserve the item name, quantity, and unit when provided. "
    "Use only information stated or clearly implied. "
    "Leave unknown optional fields as None."
    )
)


def parse_shopping_message(message: str) -> ShoppingItems:
    result = agent.run_sync(message)
    return result.output


if __name__ == "__main__":
    test_messages = [
    "Add milk and 2 kg rice to my shopping list.",
    "Buy tomoatoes."
]
    for msg in test_messages:
        item = parse_shopping_message(msg)
        print(item.model_dump())