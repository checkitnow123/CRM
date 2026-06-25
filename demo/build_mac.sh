#!/usr/bin/env bash
# Build CheckItNow Demo — double-click .app (macOS only)
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Installing dependencies..."
pip install -r requirements.txt -q
pip install pyinstaller pillow -q

echo "==> Building icons (.icns + logo)..."
python3 scripts/make_icon.py

echo "==> Building app bundle..."
pkill -x CheckItNow 2>/dev/null || true
sleep 1
export PYTHONPATH=""
pyinstaller --noconfirm --clean CheckItNow.spec

APP_SRC="dist/CheckItNow.app"
if [[ ! -d "$APP_SRC" ]]; then
    echo "Build failed — CheckItNow.app not found at $APP_SRC" >&2
    exit 1
fi

STAGING="dist/CheckItNow"
mkdir -p "$STAGING"
rm -rf "$STAGING/CheckItNow.app"
mv "$APP_SRC" "$STAGING/"

mkdir -p "$STAGING/data/backups/daily" "$STAGING/data/backups/recent" "$STAGING/config"
if [[ ! -f "$STAGING/data/clients.json" ]]; then
    printf '[]\n' > "$STAGING/data/clients.json"
fi
cp -f config/* "$STAGING/config/"

readme="$STAGING/README.txt"
cat > "$readme" <<'EOF'
CheckItNow Demo (macOS)
=======================

1. Double-click CheckItNow.app
2. Your data is saved in the data folder next to this app
3. Backups: data/backups/ (automatic daily rolling)
4. Branding: edit config/branding.json and web/assets/logo.svg

Sign-in (when collaboration is enabled): admin/admin, user/user

Forgot password:
  - Settings > Account password (change your own while signed in)
  - Settings > Admin: reset user password (admin only)
  - Or edit config/collab.json on this Mac (demo stores passwords in plain text)

Requires: macOS 12+ (Monterey or later), Apple Silicon or Intel.
First launch: if macOS blocks the app, right-click CheckItNow.app → Open.
For distribution, code signing and notarization are recommended.
EOF

echo ""
echo "SUCCESS: $STAGING/CheckItNow.app"
echo "Zip the entire folder dist/CheckItNow/ for distribution."
echo ""
