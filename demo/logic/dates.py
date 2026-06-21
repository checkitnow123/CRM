"""Date / urgency helpers."""

from __future__ import annotations

from datetime import date, timedelta

from logic.alert_settings import load_alert_settings
from logic.constants import MODE_MILESTONE
from logic.i18n import t


def today() -> date:
    return date.today()


def format_end_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def days_remaining(end: date) -> int:
    return (end - today()).days


def urgency_tier(days: int) -> str:
    if days < 0:
        return "expired"
    tier = countdown_tier(days)
    if tier == "urgent":
        return "critical"
    if tier == "critical":
        return "urgent"
    if tier == "warning":
        return "urgent"
    return "ok"


def _thresholds() -> dict[str, int]:
    return load_alert_settings()


def countdown_tier(days: int) -> str:
    """Visual tier for countdown badge / card stripe."""
    s = _thresholds()
    if days < 0:
        return "expired"
    if days <= s["urgent_days"]:
        return "urgent"
    if days <= s["critical_days"]:
        return "critical"
    if days <= s["warning_days"]:
        return "warning"
    return "ok"


def status_badge_tier(days: int) -> str:
    if days < 0:
        return "expired"
    tier = countdown_tier(days)
    if tier == "urgent":
        return "urgent"
    if tier in ("critical", "warning"):
        return "warning"
    return "healthy"


def status_badge_label(L: str, tier: str) -> str:
    from logic.i18n import strip_emoji

    return strip_emoji(t(L, f"badge_{tier}"))


def urgency_label(days: int, L: str) -> str:
    tier = urgency_tier(days)
    if tier == "expired":
        return t(L, "status_expired", n=abs(days))
    if tier == "critical":
        return t(L, "status_critical", n=days)
    if tier == "urgent":
        return t(L, "status_urgent", n=days)
    return t(L, "status_ok", n=days)


def days_display(days: int, L: str) -> str:
    if days < 0:
        return t(L, "days_over", n=abs(days))
    return t(L, "days_left", n=days)


def urgency_color(days: int) -> str:
    tier = countdown_tier(days)
    return {
        "expired": "#FF3B30",
        "urgent": "#FF3B30",
        "critical": "#FF6B00",
        "warning": "#FF9500",
        "ok": "#34C759",
    }[tier]


def next_date_info(client: dict, L: str) -> tuple[str, str, date | None]:
    from logic.milestones import milestone_all_complete, next_scheduled_visit

    if client["mode"] != MODE_MILESTONE:
        d = client["end_date"]
        return "next_payment", format_end_date(d), d

    if milestone_all_complete(client):
        return "next_visit", t(L, "all_sessions_done"), None

    nxt = next_scheduled_visit(client)
    if not nxt:
        return "next_visit", "—", None
    idx, nxt_d = nxt
    label = t(L, "next_visit")
    return "next_visit", format_end_date(nxt_d), nxt_d
