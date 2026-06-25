#!/usr/bin/env bash
# Package CheckItNow for Itch.io — clean macOS folder + zip
set -euo pipefail
cd "$(dirname "$0")"

VERSION="1.6.0"
SOURCE="dist/CheckItNow"
STAGING="release/CheckItNow-Mac"
OUT_DIR="release"
ZIP_PATH="$OUT_DIR/CheckItNow-Mac-v${VERSION}.zip"

if [[ ! -d "$SOURCE/CheckItNow.app" ]]; then
    echo "Build not found. Run ./build_mac.sh first (outputs to dist/CheckItNow)" >&2
    exit 1
fi

echo "==> Staging release folder..."
rm -rf "$STAGING"
mkdir -p "$STAGING"
cp -R "$SOURCE/." "$STAGING/"

cp -f config/* "$STAGING/config/"

data="$STAGING/data"
rm -f "$data/startup.log" "$data/activity_log.json" 2>/dev/null || true
rm -f "$data/backups/daily/"* "$data/backups/recent/"* 2>/dev/null || true
mkdir -p "$data/backups/daily" "$data/backups/recent"
printf '[]\n' > "$data/clients.json"

branding="$STAGING/config/branding.json"
if [[ -f "$branding" ]]; then
    python3 - "$branding" "$VERSION" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
version = sys.argv[2]
data = json.loads(path.read_text(encoding="utf-8"))
data["footerNote"] = (
    f"Licensed desktop CRM v{version} - support: checkitnow123@gmail.com"
)
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY
fi

itch_dir="$(cd .. && pwd)/go-to-market/itch-io"
cp -f "$itch_dir/EULA.txt" "$STAGING/"
cp -f "$itch_dir/README-Mac.txt" "$STAGING/README.txt"

echo "==> Creating zip..."
mkdir -p "$OUT_DIR"
rm -f "$ZIP_PATH"
ditto -c -k --sequesterRsrc --keepParent "$STAGING" "$ZIP_PATH"

echo ""
echo "SUCCESS"
echo "  Folder: $STAGING"
echo "  Zip:    $ZIP_PATH"
echo ""
echo "Upload the ZIP to Itch.io alongside the Windows build."
echo "Listing copy: go-to-market/itch-io/ITCH_PAGE_COPY.md"
echo ""
