"""Native helpers exposed to the embedded WebView (save dialogs, etc.)."""

from __future__ import annotations

import base64
from typing import Any

import webview
from webview import FileDialog


class DesktopApi:
    def save_excel_export(self, data_b64: str, suggested_name: str) -> dict[str, Any]:
        """Show a Save As dialog and write the exported workbook."""
        if not webview.windows:
            return {"ok": False, "error": "no_window"}
        win = webview.windows[0]
        default_name = (suggested_name or "CheckItNow-clients.xlsx").strip()
        if not default_name.lower().endswith(".xlsx"):
            default_name += ".xlsx"
        chosen = win.create_file_dialog(
            FileDialog.SAVE,
            save_filename=default_name,
            file_types=("Excel workbook (*.xlsx)", "All files (*.*)"),
        )
        if not chosen:
            return {"ok": False, "cancelled": True}
        path = chosen[0] if isinstance(chosen, (tuple, list)) else str(chosen)
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"
        try:
            with open(path, "wb") as f:
                f.write(base64.b64decode(data_b64))
        except OSError as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "path": path}

    def show_notification(self, title: str, message: str) -> dict[str, Any]:
        from logic.notifications import show_desktop_toast

        ok = show_desktop_toast(str(title or ""), str(message or ""))
        return {"ok": ok}

    def pick_data_folder(self, initial_dir: str = "") -> dict[str, Any]:
        """Native folder picker for Dropbox / shared data directory."""
        if not webview.windows:
            return {"ok": False, "error": "no_window"}
        win = webview.windows[0]
        start = (initial_dir or "").strip()
        kwargs: dict[str, Any] = {}
        if start:
            kwargs["directory"] = start
        chosen = win.create_file_dialog(FileDialog.FOLDER, **kwargs)
        if not chosen:
            return {"ok": False, "cancelled": True}
        path = chosen[0] if isinstance(chosen, (tuple, list)) else str(chosen)
        return {"ok": True, "path": path}
