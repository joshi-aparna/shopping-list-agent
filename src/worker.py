import json
import logging
import os
import shutil
import time
from pathlib import Path
import logging.handlers
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid

from .shopping_service import process_shopping_message

load_dotenv()
PENDING_MESSAGES_PARENT_DIR = Path(os.environ["PENDING_MESSAGES_PARENT_DIR"])
PENDING_DIR = PENDING_MESSAGES_PARENT_DIR / "pending"
COMPLETED_DIR = PENDING_MESSAGES_PARENT_DIR / "completed"
FAILED_DIR = PENDING_MESSAGES_PARENT_DIR / "failed"
POLL_INTERVAL = 1
LOG_DIR = Path(__file__).resolve().parent.parent / "Logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


handler = logging.handlers.RotatingFileHandler(
    LOG_DIR / "worker.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,
    encoding="utf-8",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[handler],
)

def process_file(path: Path) -> None:
    try:
        with path.open("r", encoding="utf-8") as file:
            task = json.load(file)

        message = task["text"]
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Task text must be a non-empty string")

        count = process_shopping_message(message)

        move_to_daily_folder(path, COMPLETED_DIR)

        logging.info(
            "Processed task %s: %d shopping items created",
            task.get("task_id", path.name),
            count,
        )
        write_notification(
            f"Successfully processed your message: {task.get('text', '')}",
        )

    except Exception:
        logging.exception("Failed to process %s", path.name)
        write_notification(
            f"Failed to process your message: {task.get('text', '')}",
        )

        if path.exists():
            try:
                move_to_daily_folder(path, FAILED_DIR)
            except OSError:
                logging.exception("Could not move %s to failed", path.name)


def write_notification(message: str) -> None:
    notification = {
        "text": message,
        "try_count": 0,
    }
    timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}-{uuid.uuid4().hex[:4]}.json"
    path = PENDING_MESSAGES_PARENT_DIR / "sendmessage" / filename
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(notification, file, ensure_ascii=False, indent=2)

def move_to_daily_folder(path, destination):
    day = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
    folder = destination / day
    folder.mkdir(parents=True, exist_ok=True)
    os.replace(path, folder / path.name)

def main() -> None:
    COMPLETED_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.info("Watching %s", PENDING_DIR)

    while True:
        files = sorted(PENDING_DIR.glob("*.json"))

        if not files:
            time.sleep(POLL_INTERVAL)
            continue

        for path in files:
            process_file(path)


if __name__ == "__main__":
    main()