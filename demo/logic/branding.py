"""Load per-client branding — swap config/branding.json + assets for each customer."""

from __future__ import annotations

import json
from pathlib import Path

from logic.paths import config_dir

CONFIG_DIR = config_dir()
DEFAULT_BRANDING = {
    "appName": "CheckItNow",
    "tagline": "Universal solopreneur & service CRM",
    "subtitle": "Track clients, sessions, and milestones — tutors, coaches, techs, therapists, anyone.",
    "logo": "/assets/logo.svg",
    "logoAlt": "CheckItNow",
    "primaryColor": "#007AFF",
    "footerNote": "Demo — data saved locally in data/clients.json",
}


def load_branding() -> dict:
    path = CONFIG_DIR / "branding.json"
    if not path.exists():
        return dict(DEFAULT_BRANDING)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    merged = dict(DEFAULT_BRANDING)
    merged.update(data)
    return merged
