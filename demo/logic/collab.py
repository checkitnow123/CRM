"""Shared-folder collaboration — login, editor lock, viewer (read-only) sessions."""

from __future__ import annotations

import json
import os
import secrets
import socket
import threading
from datetime import datetime, timedelta, timezone
from typing import Any

from logic.paths import config_dir, data_dir

CONFIG_PATH = config_dir() / "collab.json"
LOCK_PATH = data_dir() / "editing.lock"
ADMIN_USERNAME = "admin"
MIN_PASSWORD_LEN = 4

DEFAULT_CONFIG: dict[str, Any] = {
    "enabled": True,
    "users": {
        "admin": "admin",
        "user": "user",
    },
    "lock_stale_minutes": 30,
    "heartbeat_interval_seconds": 120,
}

_sessions: dict[str, dict[str, Any]] = {}
_sessions_lock = threading.Lock()
_memory_lock: dict[str, Any] | None = None
_disk_lock_ready = False


def _load_lock_from_disk() -> dict[str, Any] | None:
    if not LOCK_PATH.exists():
        return None
    try:
        data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _warm_lock_from_disk() -> None:
    global _memory_lock, _disk_lock_ready
    try:
        _memory_lock = _load_lock_from_disk()
    finally:
        _disk_lock_ready = True


threading.Thread(target=_warm_lock_from_disk, daemon=True, name="collab-lock-warm").start()


def _sync_lock_to_disk(data: dict[str, Any] | None) -> None:
    def _worker() -> None:
        if data is None:
            try:
                LOCK_PATH.unlink(missing_ok=True)
            except OSError:
                pass
            return
        try:
            LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
            LOCK_PATH.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except OSError:
            pass

    threading.Thread(target=_worker, daemon=True, name="collab-lock-sync").start()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(value: str) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def load_collab_config() -> dict[str, Any]:
    raw: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            raw = {}
    out = dict(DEFAULT_CONFIG)
    if isinstance(raw.get("enabled"), bool):
        out["enabled"] = raw["enabled"]
    users = raw.get("users")
    if isinstance(users, dict) and users:
        cleaned: dict[str, str] = {}
        for key, val in users.items():
            if isinstance(key, str) and isinstance(val, str) and key.strip():
                cleaned[key.strip()] = val
        if cleaned:
            out["users"] = cleaned
    stale = raw.get("lock_stale_minutes")
    if isinstance(stale, int) and stale >= 5:
        out["lock_stale_minutes"] = min(stale, 24 * 60)
    interval = raw.get("heartbeat_interval_seconds")
    if isinstance(interval, int) and interval >= 30:
        out["heartbeat_interval_seconds"] = min(interval, 3600)
    return out


def save_collab_config(patch: dict[str, Any]) -> dict[str, Any]:
    current = load_collab_config()
    if isinstance(patch.get("enabled"), bool):
        current["enabled"] = patch["enabled"]
    CONFIG_PATH.write_text(
        json.dumps(current, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return current


def _save_users(users: dict[str, str]) -> None:
    current = load_collab_config()
    current["users"] = users
    CONFIG_PATH.write_text(
        json.dumps(current, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def list_usernames() -> list[str]:
    users = load_collab_config().get("users") or {}
    return sorted(str(name) for name in users.keys())


def change_password(username: str, current_password: str, new_password: str) -> tuple[bool, str]:
    name = username.strip()
    new_pw = new_password or ""
    if len(new_pw) < MIN_PASSWORD_LEN:
        return False, "password_too_short"
    if not verify_user(name, current_password):
        return False, "invalid_credentials"
    users = dict(load_collab_config().get("users") or {})
    if name not in users:
        return False, "user_not_found"
    users[name] = new_pw
    _save_users(users)
    return True, "ok"


def admin_reset_password(
    admin_username: str,
    admin_password: str,
    target_username: str,
    new_password: str,
) -> tuple[bool, str]:
    admin = admin_username.strip()
    target = target_username.strip()
    new_pw = new_password or ""
    if admin != ADMIN_USERNAME:
        return False, "not_admin"
    if len(new_pw) < MIN_PASSWORD_LEN:
        return False, "password_too_short"
    if not verify_user(admin, admin_password):
        return False, "invalid_credentials"
    users = dict(load_collab_config().get("users") or {})
    if target not in users:
        return False, "user_not_found"
    users[target] = new_pw
    _save_users(users)
    return True, "ok"


def collab_enabled() -> bool:
    if os.environ.get("PUBLIC_DEMO", "").strip() in ("1", "true", "yes"):
        return False
    return bool(load_collab_config().get("enabled"))


def verify_user(username: str, password: str) -> bool:
    users = load_collab_config().get("users") or {}
    expected = users.get(username.strip())
    return isinstance(expected, str) and secrets.compare_digest(expected, password)


def _hostname() -> str:
    try:
        return socket.gethostname() or "unknown"
    except OSError:
        return "unknown"


def read_lock() -> dict[str, Any] | None:
    if _memory_lock is None:
        return None
    return dict(_memory_lock)


def _lock_is_stale(lock: dict[str, Any] | None) -> bool:
    if not lock:
        return True
    cfg = load_collab_config()
    stale_min = int(cfg.get("lock_stale_minutes") or 30)
    heartbeat = _parse_iso(str(lock.get("heartbeat") or lock.get("since") or ""))
    if heartbeat is None:
        return True
    return _now() - heartbeat > timedelta(minutes=stale_min)


def _active_session_tokens() -> set[str]:
    with _sessions_lock:
        return set(_sessions.keys())


def _demote_session_token(token: str) -> None:
    with _sessions_lock:
        sess = _sessions.get(token)
        if sess:
            sess["can_write"] = False
            sess["role"] = "viewer"


def _lock_is_reclaimable(lock: dict[str, Any] | None, *, login_username: str = "") -> bool:
    if not lock or _lock_is_stale(lock):
        return False
    if lock.get("machine") != _hostname():
        return False
    token = lock.get("session_token")
    if not token:
        return True
    if token not in _active_session_tokens():
        return True
    if login_username and lock.get("username") == login_username:
        return True
    return False


def _lock_holder_view(lock: dict[str, Any] | None, viewer_token: str = "") -> dict[str, Any] | None:
    if not lock or _lock_is_stale(lock):
        return None
    reclaimable = _lock_is_reclaimable(lock)
    return {
        "username": lock.get("username", ""),
        "machine": lock.get("machine", ""),
        "since": lock.get("since", ""),
        "heartbeat": lock.get("heartbeat", ""),
        "is_you": lock.get("session_token") == viewer_token,
        "reclaimable": reclaimable,
    }


def _write_lock(data: dict[str, Any]) -> None:
    global _memory_lock
    _memory_lock = dict(data)
    _sync_lock_to_disk(_memory_lock)


def _delete_lock_file() -> None:
    global _memory_lock
    _memory_lock = None
    _sync_lock_to_disk(None)


def _clear_lock_if_token(token: str) -> None:
    lock = read_lock()
    if lock and lock.get("session_token") == token:
        _delete_lock_file()


def try_acquire_lock(username: str, session_token: str) -> tuple[bool, dict[str, Any] | None]:
    existing = read_lock()
    if existing and not _lock_is_stale(existing):
        if existing.get("session_token") == session_token:
            return True, existing
        if _lock_is_reclaimable(existing, login_username=username):
            old_token = existing.get("session_token")
            if old_token:
                _demote_session_token(str(old_token))
            _delete_lock_file()
        else:
            return False, existing
    elif existing and _lock_is_stale(existing):
        _delete_lock_file()

    now = _now()
    payload = {
        "username": username,
        "machine": _hostname(),
        "session_token": session_token,
        "since": _iso(now),
        "heartbeat": _iso(now),
    }
    _write_lock(payload)
    return True, payload


def refresh_lock(session_token: str) -> bool:
    lock = read_lock()
    if not lock or lock.get("session_token") != session_token:
        return False
    if _lock_is_stale(lock):
        return False
    lock["heartbeat"] = _iso(_now())
    _write_lock(lock)
    return True


def release_lock(session_token: str) -> None:
    _clear_lock_if_token(session_token)


def force_release_lock(username: str, password: str) -> tuple[bool, str]:
    if not verify_user(username, password):
        return False, "invalid_credentials"
    _delete_lock_file()
    with _sessions_lock:
        for token, sess in list(_sessions.items()):
            if sess.get("role") == "editor" or sess.get("can_write"):
                sess["role"] = "viewer"
                sess["can_write"] = False
    return True, "released"


def _session_payload(token: str, sess: dict[str, Any]) -> dict[str, Any]:
    lock = read_lock()
    holder = _lock_holder_view(lock, token)
    reclaimable = bool(holder and holder.get("reclaimable"))
    return {
        "authenticated": True,
        "token": token,
        "username": sess.get("username", ""),
        "role": sess.get("role", "viewer"),
        "can_write": bool(sess.get("can_write")),
        "machine": sess.get("machine", ""),
        "collab_enabled": collab_enabled(),
        "lock_holder": holder,
        "lock_stale": _lock_is_stale(lock),
        "lock_reclaimable": reclaimable,
    }


def login(username: str, password: str, role: str) -> tuple[dict[str, Any] | None, str | None]:
    username = username.strip()
    role = role.strip().lower()
    if role not in ("editor", "viewer"):
        role = "viewer"
    if not verify_user(username, password):
        return None, "invalid_credentials"

    token = secrets.token_urlsafe(24)
    machine = _hostname()
    can_write = False
    lock_info: dict[str, Any] | None = None

    if role == "editor":
        ok, lock_info = try_acquire_lock(username, token)
        if not ok:
            role = "viewer"
        else:
            can_write = True

    sess = {
        "username": username,
        "role": role,
        "can_write": can_write,
        "machine": machine,
        "created_at": _iso(_now()),
    }
    with _sessions_lock:
        _sessions[token] = sess

    payload = _session_payload(token, sess)
    if role == "viewer" and lock_info and not can_write:
        payload["requested_editor"] = True
        payload["editor_blocked"] = True
    return payload, None


def promote_to_editor(token: str) -> tuple[dict[str, Any] | None, str | None]:
    with _sessions_lock:
        sess = _sessions.get(token)
        if not sess:
            return None, "not_authenticated"
        if sess.get("can_write"):
            snap = dict(sess)
        else:
            snap = None
            username = sess.get("username", "")
    if snap:
        return _session_payload(token, snap), None

    ok, _lock_info = try_acquire_lock(username, token)
    if not ok:
        return None, "lock_held"

    with _sessions_lock:
        sess = _sessions.get(token)
        if not sess:
            return None, "not_authenticated"
        sess["role"] = "editor"
        sess["can_write"] = True
        snap = dict(sess)
    return _session_payload(token, snap), None


def demote_to_viewer(token: str) -> tuple[dict[str, Any] | None, str | None]:
    with _sessions_lock:
        sess = _sessions.get(token)
        if not sess:
            return None, "not_authenticated"
        was_editor = bool(sess.get("can_write"))
    if was_editor:
        release_lock(token)
    with _sessions_lock:
        sess = _sessions.get(token)
        if not sess:
            return None, "not_authenticated"
        sess["role"] = "viewer"
        sess["can_write"] = False
        snap = dict(sess)
    return _session_payload(token, snap), None


def logout(token: str) -> None:
    with _sessions_lock:
        sess = _sessions.pop(token, None)
    if not sess:
        return
    if sess.get("can_write"):
        release_lock(token)
        return

    lock = read_lock()
    if not lock:
        return
    lock_token = lock.get("session_token")
    lock_user = lock.get("username")
    if lock_token == token:
        _delete_lock_file()
        return
    if lock_user and lock_user == sess.get("username") and _lock_is_reclaimable(lock):
        _delete_lock_file()


def get_session(token: str | None) -> dict[str, Any] | None:
    if not token:
        return None
    with _sessions_lock:
        sess = _sessions.get(token)
        return dict(sess) if sess else None


def demote_session_if_lock_lost(token: str) -> dict[str, Any] | None:
    with _sessions_lock:
        sess = _sessions.get(token)
        if not sess or not sess.get("can_write"):
            return dict(sess) if sess else None
    if refresh_lock(token):
        return get_session(token)
    with _sessions_lock:
        sess = _sessions.get(token)
        if sess:
            sess["can_write"] = False
            sess["role"] = "viewer"
            return dict(sess)
    return None


def session_status(token: str | None) -> dict[str, Any]:
    cfg = load_collab_config()
    enabled = bool(cfg.get("enabled"))
    base: dict[str, Any] = {
        "collab_enabled": enabled,
        "authenticated": False,
        "can_write": not enabled,
        "role": "editor" if not enabled else "",
        "username": "",
        "lock_holder": None,
        "lock_stale": True,
        "lock_reclaimable": False,
        "heartbeat_interval_seconds": int(cfg.get("heartbeat_interval_seconds") or 120),
        "demo_users_hint": "",
    }
    if not enabled:
        return base

    users = cfg.get("users") or {}
    if users:
        base["demo_users_hint"] = ", ".join(sorted(users.keys()))

    sess = get_session(token)
    if sess and sess.get("can_write"):
        sess = demote_session_if_lock_lost(token) or sess
    if not sess:
        lock = read_lock()
        holder = _lock_holder_view(lock)
        base["lock_holder"] = holder
        base["lock_stale"] = _lock_is_stale(lock)
        base["lock_reclaimable"] = bool(holder and holder.get("reclaimable"))
        return base

    return _session_payload(token or "", sess)


def session_can_write(token: str | None) -> bool:
    if not collab_enabled():
        return True
    sess = get_session(token)
    return bool(sess and sess.get("can_write"))
