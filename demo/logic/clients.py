"""Client persistence and CRUD."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from logic.alerts import (
    effective_alert_days,
    is_alert_snoozed,
    is_expired_kpi,
    is_urgent_kpi,
    needs_priority_alert,
    parse_snooze,
)
from logic.constants import MODE_MILESTONE, MODE_SINGLE, ACCOUNT_ACTIVE, ACCOUNT_CLOSED
from logic.dates import days_remaining, format_end_date, today
from logic.i18n import mode_label, t
from logic.milestones import (
    apply_milestone_schedule,
    build_milestone_dates,
    ensure_milestone_dates,
    ensure_milestone_schedule,
    milestone_all_complete,
    milestone_done_count,
    milestone_history_text,
    milestone_service_label,
    new_id,
    next_scheduled_visit,
    schedule_rows,
    set_milestone_checked,
    is_routine_next_month,
)
from logic.backup import (
    atomic_write_clients_json,
    load_clients_json_with_recovery,
    refresh_daily_snapshot,
    snapshot_existing_clients_file,
)

from logic.paths import data_dir

DATA_DIR = data_dir()
CLIENTS_FILE = DATA_DIR / "clients.json"


def _default_clients() -> list[dict[str, Any]]:
    t0 = today()
    return [
        {
            "id": new_id(),
            "mode": MODE_SINGLE,
            "client_name": "Student Mary",
            "contact_name": "Mary",
            "client_email": "mary@example.com",
            "service_label": "English Tutoring Package",
            "end_date": format_end_date(t0 + timedelta(days=14)),
            "start_date": format_end_date(t0),
            "total_milestones": None,
            "completed_milestones": None,
            "milestone_dates": None,
        },
        {
            "id": new_id(),
            "mode": MODE_SINGLE,
            "client_name": "Gym Client Alex",
            "contact_name": "Alex",
            "client_email": "alex@example.com",
            "service_label": "10-Session Personal Training",
            "end_date": format_end_date(t0 + timedelta(days=52)),
            "start_date": format_end_date(t0),
            "total_milestones": None,
            "completed_milestones": None,
            "milestone_dates": None,
        },
        {
            "id": new_id(),
            "mode": MODE_MILESTONE,
            "client_name": "Wellness Co.",
            "contact_name": "Gary Lin",
            "client_email": "gary@wellness.co",
            "service_label": "10-Session Yoga Program",
            "end_date": format_end_date(t0 + timedelta(days=90)),
            "start_date": format_end_date(t0),
            "total_milestones": 10,
            "completed_milestones": 3,
            "milestone_dates": build_milestone_dates(10, 3, t0),
        },
        {
            "id": new_id(),
            "mode": MODE_MILESTONE,
            "client_name": "Acme Corp",
            "contact_name": "Diana Ho",
            "client_email": "diana@acme.com",
            "service_label": "CCTV Quarterly Maintenance",
            "end_date": format_end_date(t0 + timedelta(days=8)),
            "start_date": format_end_date(t0),
            "total_milestones": 4,
            "completed_milestones": 2,
            "milestone_dates": build_milestone_dates(4, 2, t0),
        },
    ]


def _parse_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        return date.fromisoformat(value[:10])
    return today()


def normalize_group(value: Any) -> str:
    return str(value or "").strip()


def normalize_client_numbers(raw: Any) -> list[str]:
    if not raw:
        return []
    parts: list[str] = []
    if isinstance(raw, str):
        parts = raw.replace("\n", ",").replace(";", ",").split(",")
    elif isinstance(raw, list):
        parts = [str(p) for p in raw]
    seen: set[str] = set()
    out: list[str] = []
    for part in parts:
        num = str(part).strip()
        if num and num not in seen:
            seen.add(num)
            out.append(num)
    return out


def client_matches_query(client: dict[str, Any], query: str) -> bool:
    q = query.strip().lower()
    if not q:
        return True
    haystack = [
        client.get("client_name", ""),
        client.get("contact_name", ""),
        client.get("client_email", ""),
        client.get("service_label", ""),
        client.get("group", ""),
        *(client.get("client_numbers") or []),
    ]
    return any(q in str(item).lower() for item in haystack if item)


def list_client_groups(clients: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    groups: list[str] = []
    for client in clients:
        group = normalize_group(client.get("group"))
        if group and group not in seen:
            seen.add(group)
            groups.append(group)
    return sorted(groups, key=str.lower)


def is_client_closed(client: dict[str, Any]) -> bool:
    return (client.get("account_status") or ACCOUNT_ACTIVE) == ACCOUNT_CLOSED


def active_clients(clients: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [c for c in clients if not is_client_closed(c)]


def normalize_client(raw: dict[str, Any]) -> dict[str, Any]:
    client = dict(raw)
    client.setdefault("contact_name", "")
    client.setdefault("client_email", "")
    client.setdefault("group", "")
    client.setdefault("client_numbers", [])
    client.setdefault("account_status", ACCOUNT_ACTIVE)
    client.setdefault("closed_at", None)
    if client.get("account_status") not in (ACCOUNT_ACTIVE, ACCOUNT_CLOSED):
        client["account_status"] = ACCOUNT_ACTIVE
    client["group"] = normalize_group(client.get("group"))
    client["client_numbers"] = normalize_client_numbers(client.get("client_numbers"))
    client.setdefault("alert_snoozed_until", None)
    client.setdefault("last_reminder_at", None)
    client.setdefault("milestone_schedule", None)
    if client.get("mode") == MODE_MILESTONE:
        ensure_milestone_schedule(client)
    snooze = parse_snooze(client.get("alert_snoozed_until"))
    client["alert_snoozed_until"] = format_end_date(snooze) if snooze else None
    client["end_date"] = _parse_date(client.get("end_date"))
    client["start_date"] = _parse_date(client.get("start_date"))
    if client.get("mode") == MODE_MILESTONE:
        ensure_milestone_dates(client)
    return client


def serialize_client(client: dict[str, Any]) -> dict[str, Any]:
    out = dict(client)
    for key in ("end_date", "start_date"):
        if isinstance(out.get(key), date):
            out[key] = format_end_date(out[key])
    snooze = out.get("alert_snoozed_until")
    if isinstance(snooze, date):
        out["alert_snoozed_until"] = format_end_date(snooze)
    closed_at = out.get("closed_at")
    if isinstance(closed_at, date):
        out["closed_at"] = format_end_date(closed_at)
    return out


def load_clients() -> list[dict[str, Any]]:
    raw = load_clients_json_with_recovery()
    if raw is None:
        raw = []
        atomic_write_clients_json([])
    clients = [normalize_client(c) for c in raw]
    dirty = False
    for i, c in enumerate(clients):
        if c.get("mode") != MODE_MILESTONE:
            continue
        if i < len(raw) and not raw[i].get("milestone_schedule") and c.get("milestone_schedule"):
            dirty = True
    if dirty:
        save_clients(clients)
    return clients


def save_clients(clients: list[dict[str, Any]]) -> None:
    payload = [serialize_client(c) for c in clients]
    snapshot_existing_clients_file()
    atomic_write_clients_json(payload)
    refresh_daily_snapshot()


def filter_clients(clients: list[dict], flt: str) -> list[dict]:
    clients = active_clients(clients)
    if flt == "urgent":
        return [c for c in clients if is_urgent_kpi(c)]
    if flt == "expired":
        return [c for c in clients if is_expired_kpi(c)]
    if flt == "milestone":
        return [
            c for c in clients
            if c.get("mode") == MODE_MILESTONE and not milestone_all_complete(c)
        ]
    return list(clients)


def renew_client(
    client_id: str,
    new_end_date: date,
    reset_milestones: bool = False,
) -> dict[str, Any] | None:
    clients = load_clients()
    for c in clients:
        if c["id"] != client_id:
            continue
        c["end_date"] = new_end_date
        c["alert_snoozed_until"] = None
        c["account_status"] = ACCOUNT_ACTIVE
        c["closed_at"] = None
        if reset_milestones and c.get("mode") == MODE_MILESTONE:
            total = int(c.get("total_milestones") or 10)
            c["total_milestones"] = total
            c["milestone_dates"] = [None] * total
            c["completed_milestones"] = 0
            c["start_date"] = today()
        save_clients(clients)
        return c
    return None


def dismiss_alert(client_id: str, snooze_days: int = 30) -> dict[str, Any] | None:
    clients = load_clients()
    for c in clients:
        if c["id"] != client_id:
            continue
        c["alert_snoozed_until"] = format_end_date(today() + timedelta(days=snooze_days))
        save_clients(clients)
        return c
    return None


def set_client_closed(client_id: str, closed: bool) -> dict[str, Any] | None:
    clients = load_clients()
    for c in clients:
        if c["id"] != client_id:
            continue
        if closed:
            c["account_status"] = ACCOUNT_CLOSED
            c["closed_at"] = format_end_date(today())
            c["alert_snoozed_until"] = None
        else:
            c["account_status"] = ACCOUNT_ACTIVE
            c["closed_at"] = None
        save_clients(clients)
        return c
    return None


def log_reminder_sent(client_id: str) -> dict[str, Any] | None:
    clients = load_clients()
    for c in clients:
        if c["id"] != client_id:
            continue
        c["last_reminder_at"] = format_end_date(today())
        save_clients(clients)
        return c
    return None


def client_summary_row(client: dict, L: str) -> dict[str, str]:
    from logic.dates import next_date_info, status_badge_label, status_badge_tier, urgency_label

    days = days_remaining(client["end_date"])
    if client["mode"] == MODE_MILESTONE:
        done = milestone_done_count(client)
        total = int(client.get("total_milestones") or 0)
        if milestone_all_complete(client):
            detail = t(L, "all_sessions_done")
        else:
            detail = t(L, "detail_ms", done=done, total=total)
    else:
        detail = client.get("service_label") or t(L, "detail_single")
    label_key, next_display, _ = next_date_info(client, L)
    from logic.extra_i18n import extra_t

    numbers = client.get("client_numbers") or []
    closed = is_client_closed(client)
    status = extra_t(L, "status_closed") if closed else status_badge_label(L, status_badge_tier(days))
    return {
        "id": client["id"],
        "mode": client["mode"],
        "is_closed": closed,
        "client_name": client["client_name"],
        "group": client.get("group") or "—",
        "client_numbers": ", ".join(numbers) if numbers else "—",
        "client_numbers_list": numbers,
        "contact_name": client.get("contact_name") or "—",
        "client_email": client.get("client_email") or "—",
        "mode_label": mode_label(L, client["mode"]),
        "detail": detail,
        "end_date": format_end_date(client["end_date"]),
        "next": f"{t(L, label_key)}: {next_display}",
        "status": status,
        "needs_alert": needs_priority_alert(client) if not closed else False,
        "milestone_complete": milestone_all_complete(client),
        "open_compose": extra_t(L, "open_compose"),
    }


def milestone_queue(L: str) -> dict[str, list[dict]]:
    pending: list[dict] = []
    completed: list[dict] = []
    for c in load_clients():
        if is_client_closed(c):
            continue
        if c.get("mode") != MODE_MILESTONE:
            continue
        ensure_milestone_dates(c)
        done = milestone_done_count(c)
        total = int(c.get("total_milestones") or 0)
        base = client_to_view(c, L)
        if milestone_all_complete(c):
            history_block, _, _ = milestone_history_text(c, L)
            base["milestone_history"] = history_block
            completed.append(base)
            continue
        if done < total:
            base["next_milestone_label"] = milestone_service_label(done + 1, L)
            base["next_milestone_index"] = done
            pending.append(base)
    pending.sort(key=lambda x: x["days"])
    return {"pending": pending, "completed": completed}


def compute_kpi(clients: list[dict]) -> dict[str, int]:
    clients = active_clients(clients)
    urgent = sum(1 for c in clients if is_urgent_kpi(c))
    expired = sum(1 for c in clients if is_expired_kpi(c))
    ms_pending = sum(
        1
        for c in clients
        if c.get("mode") == MODE_MILESTONE and not milestone_all_complete(c)
    )
    ms_logged = sum(milestone_done_count(c) for c in clients if c["mode"] == MODE_MILESTONE)
    ms_total = sum(
        int(c.get("total_milestones") or 0)
        for c in clients
        if c["mode"] == MODE_MILESTONE
    )
    return {
        "all": len(clients),
        "urgent": urgent,
        "milestone": ms_pending,
        "milestone_logged": ms_logged,
        "milestone_total": ms_total,
        "expired": expired,
    }


def add_client(
    L: str,
    mode: str,
    client_name: str,
    contact_name: str,
    client_email: str,
    service_label: str,
    end_date: date,
    total_milestones: int = 10,
    milestone_schedule: list[str] | None = None,
    group: str = "",
    client_numbers: list[str] | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "id": new_id(),
        "mode": mode,
        "client_name": client_name.strip(),
        "contact_name": contact_name.strip(),
        "client_email": client_email.strip(),
        "group": normalize_group(group),
        "client_numbers": normalize_client_numbers(client_numbers or []),
        "service_label": service_label.strip() or t(L, "default_service"),
        "end_date": end_date,
        "start_date": today(),
        "total_milestones": None,
        "completed_milestones": 0,
        "milestone_dates": None,
        "milestone_schedule": None,
        "account_status": ACCOUNT_ACTIVE,
        "closed_at": None,
    }
    if mode == MODE_MILESTONE:
        if milestone_schedule:
            apply_milestone_schedule(entry, milestone_schedule)
        else:
            total = max(1, int(total_milestones))
            entry["total_milestones"] = total
            entry["milestone_dates"] = [None] * total
        ensure_milestone_schedule(entry)
    return normalize_client(entry)


def update_client_schedule(
    L: str,
    client_id: str,
    schedule: list[str],
) -> tuple[dict[str, Any] | None, str | None]:
    from logic.extra_i18n import extra_t

    clients = load_clients()
    for c in clients:
        if c["id"] != client_id:
            continue
        if c.get("mode") != MODE_MILESTONE:
            return None, extra_t(L, "err_schedule_mode")
        ensure_milestone_schedule(c)
        done = milestone_done_count(c)
        old = list(c.get("milestone_schedule") or [])
        cleaned: list[str] = []
        seen: set[str] = set()
        for s in schedule:
            s = s.strip()
            if not s or s in seen:
                continue
            try:
                date.fromisoformat(s[:10])
            except ValueError:
                return None, extra_t(L, "err_schedule")
            seen.add(s)
            cleaned.append(s)
        if len(cleaned) < done:
            return None, extra_t(L, "err_schedule_done")
        merged = list(cleaned)
        for i in range(min(done, len(old), len(merged))):
            merged[i] = old[i]
        apply_milestone_schedule(c, merged)
        save_clients(clients)
        return normalize_client(c), None
    return None, t(L, "err_name")


def update_client(
    L: str,
    client_id: str,
    client_name: str,
    contact_name: str,
    client_email: str,
    service_label: str,
    end_date: date,
    total_milestones: int | None = None,
    group: str = "",
    client_numbers: list[str] | None = None,
) -> str | None:
    clients = load_clients()
    name = client_name.strip()
    if not name:
        return t(L, "err_name")
    for c in clients:
        if c["id"] != client_id:
            continue
        if c.get("mode") == MODE_MILESTONE and total_milestones is not None:
            done = milestone_done_count(c)
            total = max(1, int(total_milestones))
            if total < done:
                return t(L, "err_total_ms", done=done)
            c["total_milestones"] = total
            ensure_milestone_dates(c)
        c["client_name"] = name
        c["contact_name"] = contact_name.strip()
        c["client_email"] = client_email.strip()
        c["group"] = normalize_group(group)
        c["client_numbers"] = normalize_client_numbers(client_numbers or [])
        c["service_label"] = service_label.strip() or t(L, "default_service")
        c["end_date"] = end_date
        save_clients(clients)
        return None
    return t(L, "err_name")


def delete_client_by_id(client_id: str) -> None:
    clients = [c for c in load_clients() if c["id"] != client_id]
    save_clients(clients)


def toggle_milestone(client_id: str, index: int, checked: bool) -> dict[str, Any] | None:
    clients = load_clients()
    for c in clients:
        if c["id"] == client_id:
            set_milestone_checked(c, index, checked)
            save_clients(clients)
            return c
    return None


def client_to_view(client: dict, L: str) -> dict[str, Any]:
    from logic.alert_settings import load_alert_settings
    from logic.dates import (
        countdown_tier,
        days_display,
        next_date_info,
        status_badge_label,
        status_badge_tier,
        urgency_color,
    )
    from logic.extra_i18n import extra_t

    is_ms = client["mode"] == MODE_MILESTONE
    if is_ms:
        ensure_milestone_schedule(client)
    days = effective_alert_days(client) if is_ms else days_remaining(client["end_date"])
    next_key, next_display, next_d = next_date_info(client, L)
    done = milestone_done_count(client) if is_ms else 0
    total = len(client.get("milestone_schedule") or []) if is_ms else 0
    ms_complete = milestone_all_complete(client) if is_ms else False
    history_block = ""
    if ms_complete:
        history_block, _, _ = milestone_history_text(client, L)
    tier = status_badge_tier(days)
    priority_days = load_alert_settings()["priority_days"]
    if ms_complete and days > priority_days:
        tier = "healthy"
    count_tier = countdown_tier(days)
    last_at = client.get("last_reminder_at")
    nxt = next_scheduled_visit(client) if is_ms and not ms_complete else None
    routine_flag = is_routine_next_month(client) if is_ms else False
    schedule = client.get("milestone_schedule") or []
    closed = is_client_closed(client)
    closed_at = client.get("closed_at")
    status_label = extra_t(L, "status_closed") if closed else status_badge_label(L, tier)
    status_tier = "closed" if closed else tier
    return {
        "id": client["id"],
        "mode": client["mode"],
        "is_closed": closed,
        "account_status": client.get("account_status") or ACCOUNT_ACTIVE,
        "closed_at": closed_at if isinstance(closed_at, str) else (format_end_date(closed_at) if closed_at else ""),
        "mode_label": mode_label(L, client["mode"]),
        "badge": "milestone" if is_ms else "expiry",
        "badge_text": t(L, "badge_milestone" if is_ms else "badge_single"),
        "client_name": client["client_name"],
        "group": client.get("group") or "",
        "client_numbers": list(client.get("client_numbers") or []),
        "contact_name": client.get("contact_name") or "",
        "client_email": client.get("client_email") or "",
        "service_label": client.get("service_label") or "",
        "end_date": format_end_date(client["end_date"]),
        "days": days,
        "days_display": days_display(days, L),
        "days_color": urgency_color(days),
        "countdown_tier": count_tier,
        "status_tier": status_tier,
        "status_label": status_label,
        "next_label": t(L, next_key),
        "next_display": next_display,
        "milestone_done": done,
        "milestone_total": total,
        "milestone_progress": t(L, "progress", done=done, total=total) if is_ms and total else "",
        "milestone_dates": list(client.get("milestone_dates") or []),
        "milestone_all_complete": ms_complete,
        "milestone_history": history_block,
        "needs_alert": needs_priority_alert(client) if not closed else False,
        "alert_snoozed": is_alert_snoozed(client),
        "alert_snoozed_until": client.get("alert_snoozed_until"),
        "last_reminder_at": last_at,
        "last_reminder_label": extra_t(L, "last_reminder", date=last_at) if last_at else "",
        "milestone_schedule": schedule,
        "next_planned_visit": schedule[nxt[0]] if nxt else "",
        "routine_next_month": routine_flag,
        "routine_note": extra_t(L, "routine_next_month") if routine_flag else "",
    }


def is_clients_empty() -> bool:
    raw = load_clients_json_with_recovery()
    return not raw


def seed_sample_clients() -> list[dict[str, Any]]:
    clients = [normalize_client(c) for c in _default_clients()]
    save_clients(clients)
    return clients


def clear_all_clients() -> None:
    save_clients([])


def ensure_sample_on_startup() -> bool:
    """Seed demo clients when database is empty and setting allows."""
    from logic.app_settings import load_app_settings

    if not load_app_settings().get("seed_sample_data", True):
        return False
    if not is_clients_empty():
        return False
    seed_sample_clients()
    return True
