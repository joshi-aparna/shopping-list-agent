from src.shopping_service import process_shopping_message


def test_process_shopping_message():
    count = process_shopping_message(
        "Add 2 kg rice and 1 packet of milk"
    )

    assert count == 2