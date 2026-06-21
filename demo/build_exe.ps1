# Build CheckItNow Demo — double-click EXE
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "==> Installing build tools..."
pip install pyinstaller pillow -q

Write-Host "==> Building icon (transparent background)..."
python scripts/make_icon.py
if ($LASTEXITCODE -ne 0) { throw "Icon build failed" }

Write-Host "==> Building EXE (onedir)..."
Stop-Process -Name CheckItNow -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$env:PYTHONPATH = ""
pyinstaller --noconfirm --clean CheckItNow.spec

$dist = Join-Path $PSScriptRoot "dist\CheckItNow"
$exe = Join-Path $dist "CheckItNow.exe"

if (-not (Test-Path $exe)) {
    Write-Error "Build failed - EXE not found at $exe"
}

New-Item -ItemType Directory -Force -Path "$dist\data\backups\daily", "$dist\data\backups\recent", "$dist\config" | Out-Null
if (-not (Test-Path "$dist\data\clients.json")) {
    python -c "from pathlib import Path; p=Path(r'$dist')/'data'/'clients.json'; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('[]\n', encoding='utf-8')"
}
Copy-Item -Path (Join-Path $PSScriptRoot "config\*") -Destination (Join-Path $dist "config\") -Force

$readme = @(
    "CheckItNow Demo",
    "================",
    "",
    "1. Double-click CheckItNow.exe",
    "2. Your data is saved in the data folder next to this EXE",
    "3. Backups: data/backups/ (automatic daily rolling)",
    "4. Branding: edit config/branding.json and web/assets/logo.svg",
    "",
    "Sign-in (when collaboration is enabled): admin/admin, user/user",
    "",
    "Forgot password:",
    "  - Settings > Account password (change your own while signed in)",
    "  - Settings > Admin: reset user password (admin only)",
    "  - Or edit config/collab.json on this PC (demo stores passwords in plain text)",
    "",
    "Requires: Windows 10/11 with WebView2 (usually pre-installed)."
)
Set-Content -Path (Join-Path $dist "README.txt") -Value $readme -Encoding utf8

Write-Host ""
Write-Host "SUCCESS: $exe"
Write-Host "Zip the entire folder dist\CheckItNow\ for distribution."
Write-Host ""
