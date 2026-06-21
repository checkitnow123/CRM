"""Reminder message builder."""

from __future__ import annotations

from urllib.parse import quote, urlencode

from logic.alert_settings import load_alert_settings
from logic.constants import CHANNEL_EMAIL, MODE_MILESTONE, PAYMENT_COLLECTION, PAYMENT_ROUTINE
from logic.dates import days_remaining, format_end_date, next_date_info, urgency_label
from logic.i18n import t
from logic.milestones import ensure_milestone_dates, milestone_done_count, milestone_history_text


def reminder_template_key(client: dict, channel: str, payment: str) -> str:
    mode_suffix = "ms" if client["mode"] == MODE_MILESTONE else "single"
    ch = "email" if channel == CHANNEL_EMAIL else "wa"
    suffix = "_collect" if payment == PAYMENT_COLLECTION else ""
    days = days_remaining(client["end_date"])
    settings = load_alert_settings()
    use_urgent = days < 0 or days <= settings["critical_days"]
    tone = "urgent" if use_urgent else "friendly"
    return f"msg_{ch}_{tone}_{mode_suffix}{suffix}"


def build_reminder_message(client: dict, L: str, channel: str, payment: str) -> str:
    contact = (client.get("contact_name") or "").strip() or t(L, "msg_default_contact")
    email = (client.get("client_email") or "").strip() or "—"
    company = client["client_name"]
    label = client.get("service_label") or t(L, "msg_default_label")
    days = days_remaining(client["end_date"])
    end_str = format_end_date(client["end_date"])
    _, next_str, _ = next_date_info(client, L)
    status = urgency_label(days, L)

    if client["mode"] == MODE_MILESTONE:
        ensure_milestone_dates(client)
    done = milestone_done_count(client)
    total = int(client.get("total_milestones") or 0)
    remain = max(0, total - done)
    overdue_days = abs(days) if days < 0 else days
    history_block, history_latest, _ = milestone_history_text(client, L)
    payment_note = (
        t(L, "note_prepaid") if payment == PAYMENT_ROUTINE else t(L, "note_collect")
    )
    urgent_note = t(L, "note_urgent")

    key = reminder_template_key(client, channel, payment)
    return t(
        L,
        key,
        contact=contact,
        email=email,
        company=company,
        label=label,
        end=end_str,
        next_date=next_str,
        days=overdue_days,
        done=done,
        total=total,
        remain=remain,
        status=status,
        history_block=history_block,
        history_latest=history_latest,
        history_header=t(L, "history_header"),
        payment_note=payment_note,
        urgent_note=urgent_note,
    )


def parse_email_message(message: str) -> tuple[str, str]:
    lines = message.splitlines()
    subject = ""
    body_start = 0
    if lines and lines[0].startswith("Subject:"):
        subject = lines[0][len("Subject:") :].strip()
        body_start = 1
    if body_start < len(lines) and lines[body_start].startswith("To:"):
        body_start += 1
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1
    body = "\n".join(lines[body_start:])
    return subject, body


def build_mailto_link(email: str, subject: str, body: str) -> str:
    addr = (email or "").strip()
    if not addr or addr == "—":
        return ""
    query = urlencode({"subject": subject, "body": body}, quote_via=quote)
    return f"mailto:{addr}?{query}"
