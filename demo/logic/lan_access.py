"""LAN / phone-on-WiFi access settings (config/lan_access.json)."""

from __future__ import annotations

import ipaddress
import json
import socket
from pathlib import Path
from typing import Any

from logic.paths import config_dir

CONFIG_PATH = config_dir() / "lan_access.json"
DEFAULT_PORT = 8765

DEFAULTS: dict[str, Any] = {
    "enabled": False,
    "port": DEFAULT_PORT,
}


def load_lan_settings() -> dict[str, Any]:
    data: dict[str, Any] = {}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    out = dict(DEFAULTS)
    if isinstance(data.get("enabled"), bool):
        out["enabled"] = data["enabled"]
    port = data.get("port")
    if isinstance(port, int) and 1024 <= port <= 65535:
        out["port"] = port
    return out


def save_lan_settings(enabled: bool) -> dict[str, Any]:
    current = load_lan_settings()
    current["enabled"] = enabled
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(current, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return current


def get_lan_ip() -> str | None:
    """Best-effort local IPv4 for same-WiFi phone access."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.4)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if is_private_ip(ip):
                return ip
    except OSError:
        pass
    return None


def is_loopback(host: str) -> bool:
    if not host:
        return True
    if host in ("127.0.0.1", "localhost", "::1"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def is_private_ip(host: str) -> bool:
    if not host:
        return False
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False


def lan_access_allowed(client_host: str) -> bool:
    if is_loopback(client_host):
        return True
    if not load_lan_settings().get("enabled"):
        return False
    return is_private_ip(client_host)


def build_lan_url(ip: str | None, port: int | None = None) -> str | None:
    if not ip:
        return None
    p = port if port is not None else load_lan_settings().get("port", DEFAULT_PORT)
    return f"http://{ip}:{p}/?glance=1"


def lan_status(port: int = DEFAULT_PORT) -> dict[str, Any]:
    settings = load_lan_settings()
    ip = get_lan_ip()
    enabled = bool(settings.get("enabled"))
    url = build_lan_url(ip, port) if enabled and ip else None
    return {
        "enabled": enabled,
        "ip": ip,
        "port": port,
        "url": url,
        "can_enable": ip is not None,
    }
