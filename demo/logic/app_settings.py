"""App preferences — notifications, sample data (config/app_settings.json)."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from logic.paths import config_dir, default_data_dir, ensure_data_folder_layout

CONFIG_PATH = config_dir() / "app_settings.json"

DEFAULTS: dict[str, Any] = {
    "seed_sample_data": True,
    "desktop_notifications": True,
    "notification_interval_minutes": 60,
    "last_notification_at": "",
    "last_notification_key": "",
    "data_path": "",
}


def load_app_settings() -> dict[str, Any]:
    data: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    out = dict(DEFAULTS)
    if isinstance(data.get("seed_sample_data"), bool):
        out["seed_sample_data"] = data["seed_sample_data"]
    if isinstance(data.get("desktop_notifications"), bool):
        out["desktop_notifications"] = data["desktop_notifications"]
    for key in ("notification_interval_minutes",):
        val = data.get(key)
        if isinstance(val, int) and val >= 5:
            out[key] = min(val, 24 * 60)
    for key in ("last_notification_at", "last_notification_key"):
        if isinstance(data.get(key), str):
            out[key] = data[key]
    if isinstance(data.get("data_path"), str):
        out["data_path"] = data["data_path"].strip()
    return out


def validate_data_path(raw: str) -> Path:
    cleaned = raw.strip()
    if not cleaned:
        raise ValueError("Data folder path is required.")
    path = Path(cleaned).expanduser()
    if not path.is_absolute():
        path = path.resolve()
    if path.is_file():
        raise ValueError("Path must be a folder, not a file.")
    ensure_data_folder_layout(path)
    if not os.access(path, os.W_OK):
        raise ValueError("Folder is not writable.")
    return path


def _target_data_is_empty(path: Path) -> bool:
    clients = path / "clients.json"
    if not clients.is_file() or clients.stat().st_size <= 3:
        return True
    try:
        data = json.loads(clients.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return True
    return not data


def migrate_local_data_if_needed(target: Path) -> bool:
    """Copy default local data into an empty custom folder."""
    source = default_data_dir()
    if target.resolve() == source.resolve() or not _target_data_is_empty(target):
        return False
    copied = False
    for name in ("clients.json", "activity_log.json", "editing.lock"):
        src = source / name
        if src.is_file():
            shutil.copy2(src, target / name)
            copied = True
    src_backups = source / "backups"
    dst_backups = target / "backups"
    if src_backups.is_dir():
        has_dst_backups = dst_backups.exists() and any(dst_backups.rglob("*"))
        if not has_dst_backups:
            shutil.copytree(src_backups, dst_backups, dirs_exist_ok=True)
            copied = True
    return copied


def get_data_path_info() -> dict[str, Any]:
    from logic.paths import data_dir

    configured = load_app_settings().get("data_path", "").strip()
    default = default_data_dir()
    session = data_dir()
    configured_resolved: Path | None = None
    if configured:
        try:
            configured_resolved = Path(configured).expanduser().resolve()
        except OSError:
            configured_resolved = None
    pending_restart = False
    if configured_resolved is not None:
        pending_restart = configured_resolved.resolve() != session.resolve()
    elif session.resolve() != default.resolve():
        pending_restart = True
    return {
        "data_path": configured,
        "data_path_default": str(default),
        "data_path_effective": str(session),
        "data_path_is_custom": bool(configured),
        "data_path_writable": os.access(session, os.W_OK),
        "data_path_pending_restart": pending_restart,
    }


def save_app_settings(patch: dict[str, Any]) -> dict[str, Any]:
    current = load_app_settings()
    if isinstance(patch.get("seed_sample_data"), bool):
        current["seed_sample_data"] = patch["seed_sample_data"]
    if isinstance(patch.get("desktop_notifications"), bool):
        current["desktop_notifications"] = patch["desktop_notifications"]
    val = patch.get("notification_interval_minutes")
    if isinstance(val, int) and val >= 5:
        current["notification_interval_minutes"] = min(val, 24 * 60)
    if "data_path" in patch:
        raw = patch.get("data_path")
        if raw is None:
            pass
        elif isinstance(raw, str):
            cleaned = raw.strip()
            if not cleaned:
                current["data_path"] = ""
            else:
                target = validate_data_path(cleaned)
                migrate_local_data_if_needed(target)
                current["data_path"] = str(target)
        else:
            raise ValueError("data_path must be a string.")
    CONFIG_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return current


def mark_notification_sent(key: str) -> None:
    from datetime import datetime

    current = load_app_settings()
    current["last_notification_at"] = datetime.now().isoformat(timespec="seconds")
    current["last_notification_key"] = key
    CONFIG_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
