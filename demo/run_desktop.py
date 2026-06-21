"""Desktop launcher — embedded window (for EXE packaging)."""

from __future__ import annotations

import os
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request

# PyInstaller windowed EXE has no console — uvicorn/logging need writable streams.
if getattr(sys, "frozen", False):
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")

import uvicorn

HOST = "127.0.0.1"
PORT = 8765
URL = f"http://{HOST}:{PORT}/"
SERVER_READY_TIMEOUT = 45.0


def _startup_log(message: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    try:
        from logic.paths import data_dir

        log_path = data_dir() / "startup.log"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except Exception:
        pass


def start_server() -> None:
    try:
        import asyncio

        _startup_log("Importing server…")
        from server import app

        _startup_log(f"Starting uvicorn on {HOST}:{PORT}")
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        config = uvicorn.Config(
            app,
            host=HOST,
            port=PORT,
            log_level="warning",
            access_log=False,
        )
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
        _startup_log("Server stopped")
    except Exception:
        _startup_log("Server failed:\n" + traceback.format_exc())


def wait_for_server(timeout: float = SERVER_READY_TIMEOUT) -> bool:
    deadline = time.time() + timeout
    url = f"http://{HOST}:{PORT}/api/health"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.75) as response:
                if response.status == 200:
                    _startup_log("Server ready")
                    return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(0.25)
    _startup_log("Server not ready before timeout")
    return False


def start_notification_loop() -> None:
    def _loop() -> None:
        time.sleep(15)
        while True:
            try:
                from logic.notifications import maybe_send_desktop_notification

                maybe_send_desktop_notification()
            except Exception:
                pass
            time.sleep(60)

    threading.Thread(target=_loop, daemon=True, name="notify-loop").start()


def _error_html(message: str) -> str:
    safe = (
        message.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>CheckItNow</title>
<style>body{{font-family:Segoe UI,sans-serif;padding:2rem;max-width:42rem;line-height:1.5}}
code{{background:#f3f4f6;padding:0.15rem 0.35rem;border-radius:4px}}</style></head>
<body><h1>CheckItNow could not start</h1>
<p>The local server did not respond on <code>{HOST}:{PORT}</code>.</p>
<p>{safe}</p>
<p>See <code>data/startup.log</code> next to the EXE for details, then restart the app.</p>
</body></html>"""


def main() -> None:
    if getattr(sys, "frozen", False):
        import multiprocessing

        multiprocessing.freeze_support()

    _startup_log("Launching desktop app")
    threading.Thread(target=start_server, daemon=True, name="uvicorn").start()
    start_notification_loop()

    try:
        import webview
    except ImportError:
        print("Install pywebview: pip install pywebview")
        print(f"Or open in browser: {URL}")
        if wait_for_server():
            print("Server is running.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        return

    from logic.branding import load_branding
    from desktop_api import DesktopApi

    title = load_branding().get("appName", "CheckItNow")
    ready = wait_for_server()
    window_kwargs = {
        "width": 1280,
        "height": 860,
        "min_size": (900, 640),
        "js_api": DesktopApi(),
    }
    if ready:
        webview.create_window(title, URL, **window_kwargs)
    else:
        webview.create_window(
            title,
            html=_error_html("Please close other CheckItNow windows, then try again."),
            **window_kwargs,
        )
    webview.start(debug=not getattr(sys, "frozen", False))


if __name__ == "__main__":
    main()
