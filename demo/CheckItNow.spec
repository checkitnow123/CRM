# PyInstaller spec — CheckItNow Demo (Windows EXE + macOS .app)
# Windows: pyinstaller --noconfirm CheckItNow.spec  → dist\CheckItNow\CheckItNow.exe
# macOS:    pyinstaller --noconfirm CheckItNow.spec  → dist/CheckItNow.app

# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None
root = Path(SPECPATH)
is_mac = sys.platform == "darwin"
mac_target_arch = None
if is_mac and os.environ.get("UNIVERSAL2", "1") == "1":
    mac_target_arch = "universal2"

hiddenimports = [
    "server",
    "desktop_api",
    "logic.paths",
    "logic.clients",
    "logic.branding",
    "logic.backup",
    "logic.lan_access",
    "logic.alert_settings",
    "logic.milestones",
    "logic.reminders",
    "logic.i18n",
    "logic.i18n_data",
    "logic.extra_i18n",
    "logic.alerts",
    "logic.alert_banner",
    "logic.dates",
    "logic.constants",
    "logic.export",
    "logic.import_excel",
    "logic.collab",
    "logic.app_settings",
    "logic.privacy",
    "multipart",
    "multipart.multipart",
    "logic.activity_log",
    "logic.notifications",
    "openpyxl",
    "openpyxl.styles",
    "webview",
    "qrcode",
    "qrcode.image.svg",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
]
if not is_mac:
    hiddenimports.append("winotify")

_icon_icns = root / "CheckItNow.icns"
_icon_ico = root / "CheckItNow.ico"
if is_mac and _icon_icns.exists():
    app_icon = str(_icon_icns)
elif _icon_ico.exists():
    app_icon = str(_icon_ico)
else:
    app_icon = None

a = Analysis(
    ["run_desktop.py"],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "web"), "web"),
        (str(root / "config"), "config"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CheckItNow",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=not is_mac,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=is_mac,
    target_arch=mac_target_arch,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=not is_mac,
    upx_exclude=[],
    name="CheckItNow",
)

if is_mac:
    app = BUNDLE(
        coll,
        name="CheckItNow.app",
        icon=app_icon,
        bundle_identifier="com.checkitnow.desktop",
        info_plist={
            "NSHighResolutionCapable": True,
            "CFBundleShortVersionString": "1.6.0",
            "CFBundleName": "CheckItNow",
            "NSAppleEventsUsageDescription": "CheckItNow shows local renewal reminders.",
        },
    )
