# PyInstaller spec — CheckItNow Demo
# Run: pyinstaller --noconfirm CheckItNow.spec

# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None
root = Path(SPECPATH)

a = Analysis(
    ["run_desktop.py"],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "web"), "web"),
        (str(root / "config"), "config"),
    ],
    hiddenimports=[
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
        "multipart",
        "multipart.multipart",
        "logic.activity_log",
        "logic.notifications",
        "winotify",
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
    ],
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
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(root / "CheckItNow.ico") if (root / "CheckItNow.ico").exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="CheckItNow",
)
