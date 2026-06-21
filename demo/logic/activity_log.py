"""Append-only local activity log (data/activity_log.json)."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Any

from logic.paths import data_dir

LOG_FILE = data_dir() / "activity_log.json"
MAX_ENTRIES = 500


def _read_entries() -> list[dict[str, Any]]:
    if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
        return []
    try:
        raw = json.loads(LOG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return []
    return raw if isinstance(raw, list) else []


def log_activity(
    action: str,
    *,
    client_id: str = "",
    client_name: str = "",
    detail: str = "",
) -> dict[str, Any]:
    entry = {
        "id": str(uuid.uuid4())[:8],
        "at": datetime.now().isoformat(timespec="seconds"),
        "action": action,
        "client_id": client_id,
        "client_name": client_name,
        "detail": detail,
    }
    entries = _read_entries()
    entries.insert(0, entry)
    entries = entries[:MAX_ENTRIES]
    LOG_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry


def list_activity(limit: int = 50) -> list[dict[str, Any]]:
    limit = max(1, min(int(limit or 50), 200))
    return _read_entries()[:limit]
