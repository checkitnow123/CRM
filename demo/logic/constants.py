"""Shared constants — mirrors parent app.py."""

URGENT_DAYS = 30
CRITICAL_DAYS = 14

MODE_SINGLE = "single"
MODE_MILESTONE = "milestone"

ACCOUNT_ACTIVE = "active"
ACCOUNT_CLOSED = "closed"

CHANNEL_SMS = "sms"
CHANNEL_EMAIL = "email"
ALL_CHANNELS = (CHANNEL_SMS, CHANNEL_EMAIL)

PAYMENT_ROUTINE = "routine"
PAYMENT_COLLECTION = "collection"

LANG_CODES = ("zh", "zh_cn", "en")
LANG_SHORT = {"zh": "繁", "zh_cn": "简", "en": "EN"}

KPI_SCROLL_TARGETS = {
    "all": "section-board",
    "urgent": "section-priority",
    "milestone": "section-board",
    "expired": "section-board",
}
