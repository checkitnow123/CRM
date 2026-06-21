"""Desktop expiry notifications (Windows toast when app is running)."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from logic.alerts import is_expired_kpi, is_urgent_kpi, needs_priority_alert
from logic.app_settings import load_app_settings, mark_notification_sent
from logic.clients import active_clients, load_clients
from logic.extra_i18n import extra_t


def expiry_counts() -> dict[str, int]:
    clients = active_clients(load_clients())
    urgent = sum(1 for c in clients if is_urgent_kpi(c))
    expired = sum(1 for c in clients if is_expired_kpi(c))
    priority = sum(1 for c in clients if needs_priority_alert(c))
    return {"urgent": urgent, "expired": expired, "priority": priority}


def notification_message(L: str, counts: dict[str, int]) -> tuple[str, str]:
    title = extra_t(L, "notify_title")
    urgent = counts.get("urgent", 0)
    expired = counts.get("expired", 0)
    priority = counts.get("priority", 0)
    if expired > 0:
        body = extra_t(L, "notify_body_expired", n=expired, urgent=urgent)
    elif urgent > 0:
        body = extra_t(L, "notify_body_urgent", n=urgent)
    elif priority > 0:
        body = extra_t(L, "notify_body_priority", n=priority)
    else:
        body = extra_t(L, "notify_body_clear")
    return title, body


def notification_key(counts: dict[str, int]) -> str:
    return f"e{counts.get('expired', 0)}:u{counts.get('urgent', 0)}:p{counts.get('priority', 0)}"


def should_notify_now() -> tuple[bool, dict[str, int], str, str]:
    settings = load_app_settings()
    if not settings.get("desktop_notifications", True):
        return False, {}, "", ""
    counts = expiry_counts()
    if counts["expired"] == 0 and counts["urgent"] == 0 and counts["priority"] == 0:
        return False, counts, "", ""
    interval = int(settings.get("notification_interval_minutes") or 60)
    last_at = settings.get("last_notification_at") or ""
    last_key = settings.get("last_notification_key") or ""
    key = notification_key(counts)
    if key == last_key:
        return False, counts, "", ""
    if last_at:
        try:
            prev = datetime.fromisoformat(last_at)
            if datetime.now() - prev < timedelta(minutes=interval):
                return False, counts, "", ""
        except ValueError:
            pass
    return True, counts, "", ""


def show_desktop_toast(title: str, body: str) -> bool:
    try:
        from winotify import Notification

        toast = Notification(app_id="CheckItNow", title=title, msg=body, duration="short")
        toast.show()
        return True
    except Exception:
        return False


def maybe_send_desktop_notification(L: str = "en") -> dict[str, Any]:
    ok, counts, _, _ = should_notify_now()
    if not ok:
        return {"sent": False, "counts": counts}
    title, body = notification_message(L, counts)
    sent = show_desktop_toast(title, body)
    if sent:
        mark_notification_sent(notification_key(counts))
    return {"sent": sent, "counts": counts, "title": title, "body": body}
