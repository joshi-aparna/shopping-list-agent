import json
from pathlib import Path

from src.agent import parse_shopping_message

cases_path = Path(__file__).with_name("cases.json")
cases = json.loads(cases_path.read_text())

passed = 0
total = 0

for case in cases:
    result = parse_shopping_message(case["message"]).model_dump()

    for field, expected in case["expected"].items():
        total += 1
        actual = result[field]
        ok = actual == expected

        if ok:
            passed += 1

        print(
            f"{'PASS' if ok else 'FAIL'} "
            f"| {case['message']} | {field}: "
            f"expected={expected!r}, actual={actual!r}"
        )

print(f"\nScore: {passed}/{total} fields passed ({passed / total:.1%})")