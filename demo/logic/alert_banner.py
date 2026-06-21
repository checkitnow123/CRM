"""Top-of-dashboard alert banner summary."""

from __future__ import annotations

from typing import Any

from logic.alert_settings import load_alert_settings
from logic.alerts import (
    count_routine_next_month,
    effective_alert_days,
    is_alert_snoozed,
    needs_priority_alert,
)


from logic.extra_i18n import extra_t
from logic.i18n import t


def compute_alert_banner(clients: list[dict], L: str) -> dict[str, Any]:
    settings = load_alert_settings()
    urgent_cutoff = settings["urgent_days"]
    critical_cutoff = settings["critical_days"]

    expired = 0
    urgent = 0
    critical = 0
    priority = 0
    routine_next = count_routine_next_month(clients)

    for c in clients:
        if is_alert_snoozed(c):
            continue
        days = effective_alert_days(c)
        if days < 0:
            expired += 1
        if needs_priority_alert(c):
            priority += 1
        if 0 <= days <= urgent_cutoff:
            urgent += 1
        elif 0 <= days <= critical_cutoff:
            critical += 1

    if expired > 0:
        level = "danger"
        message = extra_t(L, "banner_expired", n=expired)
    elif urgent > 0:
        level = "urgent"
        message = extra_t(L, "banner_urgent", n=urgent, days=urgent_cutoff)
    elif critical > 0:
        level = "critical"
        message = extra_t(L, "banner_critical", n=critical, days=critical_cutoff)
    elif priority > 0:
        level = "warn"
        message = extra_t(L, "banner_priority", n=priority, days=settings["priority_days"])
    elif routine_next > 0:
        level = "info"
        message = extra_t(L, "banner_routine", n=routine_next)
    else:
        return {
            "show": False,
            "level": "ok",
            "message": extra_t(L, "banner_all_clear"),
            "expired": 0,
            "urgent": 0,
            "critical": 0,
            "priority": 0,
            "routine_next": 0,
        }

    return {
        "show": True,
        "level": level,
        "message": message,
        "expired": expired,
        "urgent": urgent,
        "critical": critical,
        "priority": priority,
        "routine_next": routine_next,
        "action_label": t(L, "kpi_click_hint"),
    }
