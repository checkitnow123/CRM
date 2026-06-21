"""Translation helpers."""

from __future__ import annotations

import re

from logic.constants import LANG_CODES
from logic.i18n_data import LANG

_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE,
)


def strip_emoji(text: str) -> str:
    return _EMOJI_RE.sub("", str(text)).strip()


def _lookup_lang(L: str, key: str) -> str:
    if L not in LANG and L in LANG_CODES:
        L = "en"
    bucket = LANG.get(L) or LANG["zh"]
    if key in bucket:
        return bucket[key]
    if L == "zh_cn" and key in LANG.get("zh", {}):
        return LANG["zh"][key]
    if L != "en" and key in LANG.get("en", {}):
        return LANG["en"][key]
    return key


def t(L: str, key: str, **fmt) -> str:
    text = _lookup_lang(L, key)
    if fmt:
        try:
            return text.format(**fmt)
        except (KeyError, ValueError):
            return text
    return text


def mode_label(L: str, mode: str) -> str:
    from logic.constants import MODE_MILESTONE, MODE_SINGLE

    return t(L, "mode_milestone" if mode == MODE_MILESTONE else "mode_single")


def channel_label(L: str, channel: str) -> str:
    from logic.constants import CHANNEL_EMAIL, CHANNEL_SMS

    return t(L, "channel_email" if channel == CHANNEL_EMAIL else "channel_sms")
