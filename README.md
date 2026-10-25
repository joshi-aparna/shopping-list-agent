# Shopping Agent

A local AI agent that manages a shopping list through natural language messages sent via Telegram. The agent uses a locally hosted LLM to interpret requests and maintains a structured Notion database that can be accessed from a phone.

## Prerequisites

### 1. Notion database
- Create a Notion database for the shopping list.
- Create a Notion integration and grant it access to the database.
- Store the database ID for use by the agent in the .env file.

```
NOTION_DATA_SOURCE_ID=your_data_source_id_here
```

### 2. Store the Notion API key in macOS Keychain

Add the integration secret to Keychain:

```bash
security add-generic-password \
  -a "$(whoami)" \
  -s "shopping-agent-notion" \
  -w
```

Enter the Notion API key when prompted.

The Python agent retrieves the key using the `shopping-agent-notion` service name.

Then run notion_test.py to confirm access.

### 3. To understand how Pydantic AI is handling the raw response
Run this from project root

```
python -m pytest -s tests/test_agent_trace.py
```


### 4. Setup Launch Agent
Once local testing is done, run the worker in the background by running

```
chmod +x scripts/install_worker.sh scripts/uninstall_worker.sh

./scripts/install_worker.sh
```

To restart the background process after a code change:

```
launchctl kickstart -k gui/$(id -u)/com.shopping-agent.worker
```

## Development

Project setup and implementation instructions will be added as the agent evolves.
