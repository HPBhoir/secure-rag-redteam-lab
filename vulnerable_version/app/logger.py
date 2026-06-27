import json
from datetime import datetime
from pathlib import Path
import uuid

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def log_interaction(data: dict):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_id = uuid.uuid4().hex[:8]
    log_file = LOG_DIR / f"{timestamp}_{log_id}.json"

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return str(log_file)
