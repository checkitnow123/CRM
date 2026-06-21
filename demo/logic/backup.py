"""Daily rolling backup for local clients.json."""

from __future__ import annotations

import json
import re
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from logic.dates import today

from logic.paths import config_dir, data_dir

DATA_DIR = data_dir()
CLIENTS_FILE = DATA_DIR / "clients.json"
BACKUP_ROOT = DATA_DIR / "backups"
DAILY_DIR = BACKUP_ROOT / "daily"
RECENT_DIR = BACKUP_ROOT / "recent"
CONFIG_PATH = config_dir() / "backup_settings.json"

DAILY_NAME_RE = re.compile(r"^clients-(\d{4}-\d{2}-\d{2})\.json$")
RECENT_NAME_RE = re.compile(r"^clients-(\d{8}-\d{6})\.json$")

DEFAULTS: dict[str, Any] = {
    "enabled": True,
    "retention_days": 45,
    "recent_keep": 8,
}


def load_backup_settings() -> dict[str, Any]:
    data: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    out = dict(DEFAULTS)
    if isinstance(data.get("enabled"), bool):
        out["enabled"] = data["enabled"]
    for key in ("retention_days", "recent_keep"):
        val = data.get(key)
        if isinstance(val, int) and val > 0:
            out[key] = val
    return out


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    RECENT_DIR.mkdir(parents=True, exist_ok=True)


def _is_valid_clients_payload(raw: Any) -> bool:
    return isinstance(raw, list)


def _read_json_file(path: Path) -> list[dict[str, Any]] | None:
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None
    if not _is_valid_clients_payload(raw):
        return None
    return raw


def _daily_path(for_day: date | None = None) -> Path:
    d = for_day or today()
    return DAILY_DIR / f"clients-{d.isoformat()}.json"


def _recent_path(now: datetime | None = None) -> Path:
    ts = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    return RECENT_DIR / f"clients-{ts}.json"


def _copy_backup(src: Path, dest: Path) -> bool:
    if not src.exists() or src.stat().st_size == 0:
        return False
    try:
        _ensure_dirs()
        shutil.copy2(src, dest)
        return _read_json_file(dest) is not None
    except OSError:
        return False


def snapshot_existing_clients_file() -> None:
    """Copy current clients.json into daily + recent rings before overwrite."""
    if not load_backup_settings().get("enabled"):
        return
    if not CLIENTS_FILE.exists():
        return
    if _read_json_file(CLIENTS_FILE) is None:
        return
    _ensure_dirs()
    _copy_backup(CLIENTS_FILE, _daily_path())
    _copy_backup(CLIENTS_FILE, _recent_path())
    _prune_old_backups()


def refresh_daily_snapshot() -> None:
    """Ensure today's daily file matches the latest saved clients.json."""
    if not load_backup_settings().get("enabled"):
        return
    if _read_json_file(CLIENTS_FILE) is None:
        return
    _ensure_dirs()
    _copy_backup(CLIENTS_FILE, _daily_path())
    _prune_old_backups()


def atomic_write_clients_json(payload: list[dict[str, Any]]) -> None:
    _ensure_dirs()
    tmp = CLIENTS_FILE.with_suffix(".json.tmp")
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(CLIENTS_FILE)


def _prune_old_backups() -> None:
    settings = load_backup_settings()
    retention = int(settings.get("retention_days") or DEFAULTS["retention_days"])
    recent_keep = int(settings.get("recent_keep") or DEFAULTS["recent_keep"])
    cutoff = today() - timedelta(days=retention)

    for path in sorted(DAILY_DIR.glob("clients-*.json")):
        m = DAILY_NAME_RE.match(path.name)
        if not m:
            continue
        try:
            file_day = date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if file_day < cutoff:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass

    recent_files = sorted(
        RECENT_DIR.glob("clients-*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for path in recent_files[recent_keep:]:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


def _backup_candidates() -> list[Path]:
    paths: list[Path] = []
    paths.extend(DAILY_DIR.glob("clients-*.json"))
    paths.extend(RECENT_DIR.glob("clients-*.json"))
    uniq: dict[str, Path] = {}
    for p in paths:
        uniq[str(p.resolve())] = p
    return sorted(
        uniq.values(),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def restore_from_backup(path: Path | None = None) -> list[dict[str, Any]] | None:
    candidates = [path] if path else _backup_candidates()
    for candidate in candidates:
        if candidate is None or not candidate.exists():
            continue
        data = _read_json_file(candidate)
        if data is not None:
            atomic_write_clients_json(data)
            refresh_daily_snapshot()
            _copy_backup(CLIENTS_FILE, _recent_path())
            return data
    return None


def load_clients_json_with_recovery() -> list[dict[str, Any]] | None:
    """Return parsed clients list, attempting restore if main file is corrupt."""
    data = _read_json_file(CLIENTS_FILE)
    if data is not None:
        return data
    if not CLIENTS_FILE.exists():
        return None
    restored = restore_from_backup()
    return restored


def ensure_startup_backup() -> dict[str, Any]:
    """On app start: refresh today's daily snapshot if data file is healthy."""
    if not load_backup_settings().get("enabled"):
        return backup_status()
    data = _read_json_file(CLIENTS_FILE)
    if data is None:
        restore_from_backup()
        return backup_status()
    _ensure_dirs()
    daily = _daily_path()
    if not daily.exists():
        _copy_backup(CLIENTS_FILE, daily)
    _prune_old_backups()
    return backup_status()


def backup_status() -> dict[str, Any]:
    settings = load_backup_settings()
    latest: Path | None = None
    latest_at: str | None = None
    for path in _backup_candidates():
        if _read_json_file(path) is None:
            continue
        latest = path
        latest_at = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        break
    daily_count = sum(
        1 for p in DAILY_DIR.glob("clients-*.json") if _read_json_file(p) is not None
    )
    recent_count = sum(
        1 for p in RECENT_DIR.glob("clients-*.json") if _read_json_file(p) is not None
    )
    main_ok = _read_json_file(CLIENTS_FILE) is not None
    return {
        "enabled": bool(settings.get("enabled")),
        "retention_days": int(settings.get("retention_days") or DEFAULTS["retention_days"]),
        "recent_keep": int(settings.get("recent_keep") or DEFAULTS["recent_keep"]),
        "main_file_ok": main_ok,
        "latest_backup_at": latest_at,
        "latest_backup_name": latest.name if latest else None,
        "daily_count": daily_count,
        "recent_count": recent_count,
        "backup_dir": str(BACKUP_ROOT),
    }


def list_backups(limit: int = 20) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in _backup_candidates():
        if _read_json_file(path) is None:
            continue
        kind = "daily" if path.parent == DAILY_DIR else "recent"
        rows.append({
            "name": path.name,
            "kind": kind,
            "saved_at": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "path": str(path),
        })
        if len(rows) >= limit:
            break
    return rows
