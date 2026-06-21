"""Configurable alert thresholds (config/alert_settings.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "alert_settings.json"

DEFAULTS: dict[str, int] = {
    "priority_days": 30,
    "warning_days": 30,
    "critical_days": 14,
    "urgent_days": 7,
}


def load_alert_settings() -> dict[str, int]:
    data: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    out = dict(DEFAULTS)
    for key in DEFAULTS:
        val = data.get(key)
        if isinstance(val, (int, float)) and val >= 0:
            out[key] = int(val)
    return out
