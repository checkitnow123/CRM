"""Milestone tracking with planned visit schedules."""

from __future__ import annotations

import uuid
from datetime import date, timedelta
from typing import Any

from logic.constants import MODE_MILESTONE
from logic.dates import days_remaining, format_end_date, today
from logic.i18n import t


def new_id() -> str:
    return str(uuid.uuid4())[:8]


def ordinal_suffix(n: int) -> str:
    if 10 <= (n % 100) <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def milestone_service_label(index_1based: int, L: str) -> str:
    if L in ("zh", "zh_cn"):
        return t(L, "ms_service", n=index_1based)
    return t(L, "ms_service", n=index_1based, suffix=ordinal_suffix(index_1based))


def _parse_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def add_months(d: date, months: int) -> date:
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return date(year, month, day)


def build_schedule_intervals(first: date, count: int, months_apart: int) -> list[str]:
    if count <= 0:
        return []
    out: list[str] = []
    for i in range(count):
        out.append(format_end_date(add_months(first, months_apart * i)))
    return out


def build_milestone_dates(total: int, done: int, base: date | None = None) -> list[str | None]:
    if total <= 0:
        return []
    base = base or today()
    dates: list[str | None] = []
    for i in range(total):
        if i < done:
            dates.append(format_end_date(base - timedelta(days=7 * (done - 1 - i))))
        else:
            dates.append(None)
    return dates


def _legacy_spread_schedule(client: dict[str, Any]) -> list[str]:
    total = int(client.get("total_milestones") or 0)
    if total <= 0:
        return []
    start = _parse_date(client.get("start_date")) or today()
    end = _parse_date(client.get("end_date")) or start
    if total == 1:
        return [format_end_date(end)]
    span = max(1, (end - start).days)
    return [
        format_end_date(start + timedelta(days=round(span * (i + 1) / total)))
        for i in range(total)
    ]


def ensure_milestone_schedule(client: dict[str, Any]) -> list[str]:
    if client.get("mode") != MODE_MILESTONE:
        client["milestone_schedule"] = []
        return []

    total = int(client.get("total_milestones") or 0)
    schedule = client.get("milestone_schedule")
    if not schedule:
        if total > 0:
            schedule = _legacy_spread_schedule(client)
            client["milestone_schedule"] = schedule
        else:
            client["milestone_schedule"] = []
            return []

    schedule = [s for s in schedule if s]
    client["milestone_schedule"] = schedule
    dates_len = len(client.get("milestone_dates") or [])
    client["total_milestones"] = max(len(schedule), dates_len, total)

    completions = list(client.get("milestone_dates") or [])
    while len(completions) < len(schedule):
        completions.append(None)
    if len(completions) > len(schedule):
        completions = completions[: len(schedule)]
    client["milestone_dates"] = completions
    sync_completed_from_dates(client)

    if schedule:
        last = _parse_date(schedule[-1])
        if last:
            client["end_date"] = last
    return schedule


def ensure_milestone_dates(client: dict[str, Any]) -> list[str | None]:
    ensure_milestone_schedule(client)
    return client.get("milestone_dates") or []


def sync_completed_from_dates(client: dict[str, Any]) -> None:
    dates = client.get("milestone_dates") or []
    client["completed_milestones"] = sum(1 for d in dates if d)


def milestone_done_count(client: dict) -> int:
    if client.get("mode") != MODE_MILESTONE:
        return 0
    ensure_milestone_schedule(client)
    return int(client.get("completed_milestones") or 0)


def milestone_all_complete(client: dict) -> bool:
    if client.get("mode") != MODE_MILESTONE:
        return False
    ensure_milestone_schedule(client)
    total = len(client.get("milestone_schedule") or [])
    if total <= 0:
        return False
    return milestone_done_count(client) >= total


def next_scheduled_visit(client: dict) -> tuple[int, date] | None:
    if client.get("mode") != MODE_MILESTONE:
        return None
    ensure_milestone_schedule(client)
    schedule = client.get("milestone_schedule") or []
    completions = client.get("milestone_dates") or []
    for i, planned in enumerate(schedule):
        if i < len(completions) and completions[i]:
            continue
        d = _parse_date(planned)
        if d:
            return i, d
    return None


def days_until_next_visit(client: dict) -> int | None:
    nxt = next_scheduled_visit(client)
    if not nxt:
        return None
    return days_remaining(nxt[1])


def is_routine_next_month(client: dict) -> bool:
    nxt = next_scheduled_visit(client)
    if not nxt:
        return False
    nxt_d = nxt[1]
    tday = today()
    if nxt_d.year == tday.year and nxt_d.month == tday.month + 1:
        return True
    if tday.month == 12 and nxt_d.year == tday.year + 1 and nxt_d.month == 1:
        return True
    return False


def set_milestone_checked(client: dict, index: int, checked: bool) -> None:
    ensure_milestone_schedule(client)
    dates = client.get("milestone_dates") or []
    if index < 0 or index >= len(dates):
        return
    done = milestone_done_count(client)
    if checked:
        if index != done:
            return
        dates[index] = format_end_date(today())
    else:
        if index != done - 1:
            return
        dates[index] = None
    client["milestone_dates"] = dates
    sync_completed_from_dates(client)


def apply_milestone_schedule(client: dict, schedule: list[str]) -> None:
    iso: list[str] = []
    seen: set[str] = set()
    for s in schedule:
        d = _parse_date(s)
        if not d:
            continue
        key = format_end_date(d)
        if key in seen:
            continue
        seen.add(key)
        iso.append(key)
    client["milestone_schedule"] = iso
    client["total_milestones"] = len(iso)
    old = list(client.get("milestone_dates") or [])
    new_completions: list[str | None] = []
    for i in range(len(iso)):
        new_completions.append(old[i] if i < len(old) else None)
    client["milestone_dates"] = new_completions
    sync_completed_from_dates(client)
    if iso:
        client["end_date"] = _parse_date(iso[-1]) or client.get("end_date")


def milestone_history_text(client: dict, L: str) -> tuple[str, str, str]:
    program = client.get("service_label") or t(L, "msg_default_label")
    ensure_milestone_schedule(client)
    dates = client.get("milestone_dates") or []
    lines: list[str] = []
    latest_label = ""
    latest_date = ""
    for i, d in enumerate(dates):
        if d:
            label = milestone_service_label(i + 1, L)
            lines.append(t(L, "history_line", label=label, date=d))
            latest_label = label
            latest_date = d
    block = "\n".join(lines) if lines else t(L, "history_none")
    latest = (
        t(L, "history_latest", label=latest_label, date=latest_date, program=program)
        if latest_label
        else ""
    )
    return block, latest, latest_label


def schedule_rows(client: dict, L: str) -> list[dict[str, Any]]:
    ensure_milestone_schedule(client)
    schedule = client.get("milestone_schedule") or []
    completions = client.get("milestone_dates") or []
    done = milestone_done_count(client)
    rows: list[dict[str, Any]] = []
    for i, planned in enumerate(schedule):
        completed = completions[i] if i < len(completions) else None
        rows.append({
            "index": i,
            "label": milestone_service_label(i + 1, L),
            "planned": planned,
            "completed": completed,
            "done": bool(completed),
            "is_next": (not completed) and (i == done),
            "is_locked": (not completed) and (i > done),
        })
    return rows
