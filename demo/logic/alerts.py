"""Alert / priority queue logic."""

from __future__ import annotations

from datetime import date
from typing import Any

from logic.alert_settings import load_alert_settings
from logic.constants import MODE_MILESTONE
from logic.dates import days_remaining, today
from logic.milestones import (
    days_until_next_visit,
    is_routine_next_month,
    milestone_all_complete,
    next_scheduled_visit,
)


def parse_snooze(value: Any) -> date | None:
    if not value:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        return date.fromisoformat(value[:10])
    return None


def is_alert_snoozed(client: dict) -> bool:
    until = parse_snooze(client.get("alert_snoozed_until"))
    return until is not None and today() <= until


def _priority_days() -> int:
    return load_alert_settings()["priority_days"]


CRITICAL_BUFFER_DAYS = 14


def effective_alert_days(client: dict) -> int:
    """Days until next action: scheduled visit for milestones, else contract end."""
    if client.get("mode") == MODE_MILESTONE and not milestone_all_complete(client):
        visit_days = days_until_next_visit(client)
        if visit_days is not None:
            return visit_days
    return days_remaining(client["end_date"])


def _effective_days(client: dict) -> int:
    return effective_alert_days(client)


def needs_priority_alert(client: dict) -> bool:
    from logic.clients import is_client_closed
    if is_client_closed(client):
        return False
    if is_alert_snoozed(client):
        return False
    days = _effective_days(client)
    if days < 0:
        return True
    if days <= _priority_days():
        if client.get("mode") == MODE_MILESTONE and milestone_all_complete(client):
            if days > CRITICAL_BUFFER_DAYS:
                return False
        return True
    return False


def is_urgent_kpi(client: dict) -> bool:
    from logic.clients import is_client_closed
    if is_client_closed(client):
        return False
    if is_alert_snoozed(client):
        return False
    days = _effective_days(client)
    if days < 0:
        return False
    if days > _priority_days():
        return False
    if client.get("mode") == MODE_MILESTONE and milestone_all_complete(client):
        return days <= CRITICAL_BUFFER_DAYS
    return True


def is_expired_kpi(client: dict) -> bool:
    from logic.clients import is_client_closed
    if is_client_closed(client):
        return False
    if is_alert_snoozed(client):
        return False
    if client.get("mode") == MODE_MILESTONE and not milestone_all_complete(client):
        visit_days = days_until_next_visit(client)
        if visit_days is not None and visit_days < 0:
            return True
    return days_remaining(client["end_date"]) < 0


def count_routine_next_month(clients: list[dict]) -> int:
    from logic.clients import is_client_closed
    n = 0
    for c in clients:
        if is_client_closed(c):
            continue
        if is_alert_snoozed(c):
            continue
        if c.get("mode") == MODE_MILESTONE and is_routine_next_month(c):
            if not needs_priority_alert(c):
                n += 1
    return n
