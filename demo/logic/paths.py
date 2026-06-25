"""Resolve app / bundle paths for dev and PyInstaller EXE."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def app_root() -> Path:
    """Writable root — folder containing the launcher when packaged."""
    if is_frozen():
        exe = Path(sys.executable).resolve()
        if sys.platform == "darwin":
            # .../CheckItNow/CheckItNow.app/Contents/MacOS/CheckItNow
            return exe.parent.parent.parent.parent
        return exe.parent
    return Path(__file__).resolve().parent.parent


def bundle_root() -> Path:
    """Read-only bundled resources (web, default config templates)."""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", app_root()))
    return Path(__file__).resolve().parent.parent


def web_dir() -> Path:
    return bundle_root() / "web"


def config_dir() -> Path:
    dest = app_root() / "config"
    dest.mkdir(parents=True, exist_ok=True)
    if is_frozen():
        _seed_dir(bundle_root() / "config", dest)
    return dest


def _app_settings_path() -> Path:
    return app_root() / "config" / "app_settings.json"


def configured_data_path() -> Path | None:
    """Custom data folder from config/app_settings.json (empty = use default)."""
    cfg = _app_settings_path()
    if not cfg.is_file():
        return None
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    raw = data.get("data_path")
    if not isinstance(raw, str) or not raw.strip():
        return None
    return Path(raw.strip()).expanduser()


def default_data_dir() -> Path:
    return app_root() / "data"


_SESSION_DATA_DIR: Path | None = None


def ensure_data_folder_layout(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "backups" / "daily").mkdir(parents=True, exist_ok=True)
    (dest / "backups" / "recent").mkdir(parents=True, exist_ok=True)
    clients = dest / "clients.json"
    if not clients.exists():
        clients.write_text("[]\n", encoding="utf-8")


def data_dir() -> Path:
    global _SESSION_DATA_DIR
    if _SESSION_DATA_DIR is not None:
        return _SESSION_DATA_DIR
    override = configured_data_path()
    dest = override.resolve() if override else default_data_dir()
    ensure_data_folder_layout(dest)
    _SESSION_DATA_DIR = dest
    return dest


def _seed_dir(src: Path, dest: Path) -> None:
    if not src.is_dir():
        return
    for item in src.iterdir():
        target = dest / item.name
        if target.exists():
            continue
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
