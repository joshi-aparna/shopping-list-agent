from src.agent import agent


def test_inspect_agent_messages():
    result = agent.run_sync("Add 2 kg of tomatoes")

    for message in result.all_messages():
        print(f"\n{'=' * 20} {type(message).__name__} {'=' * 20}")
        print(message)

    print("\nValidated output:")
    print(result.output.model_dump())