"""Cloud launcher — Render / Railway / etc. Set PUBLIC_DEMO=1 (no login wall)."""

from __future__ import annotations

import os

import uvicorn

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8765"))


def main() -> None:
    os.environ.setdefault("PUBLIC_DEMO", "1")
    uvicorn.run("server:app", host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
