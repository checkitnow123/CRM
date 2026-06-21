"""Dev launcher — opens system browser."""

from __future__ import annotations

import threading
import time
import webbrowser

import uvicorn

HOST = "0.0.0.0"
PORT = 8765
URL = f"http://127.0.0.1:{PORT}/"


def main() -> None:
    threading.Thread(
        target=lambda: uvicorn.run(
            "server:app",
            host=HOST,
            port=PORT,
            log_level="info",
        ),
        daemon=True,
    ).start()
    time.sleep(0.8)
    print(f"CheckItNow Demo -> {URL}")
    webbrowser.open(URL)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
