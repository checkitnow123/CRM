"""Build CheckItNow.ico + CheckItNow.icns + web/assets/logo.png from CheckItNow-icon.png."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "CheckItNow-icon.png"
ICO = ROOT / "CheckItNow.ico"
ICNS = ROOT / "CheckItNow.icns"
LOGO = ROOT / "web" / "assets" / "logo.png"
SIZES = (256, 128, 64, 48, 32, 16)
ICNS_SPECS = [
    (16, "16x16"),
    (32, "16x16@2x"),
    (32, "32x32"),
    (64, "32x32@2x"),
    (128, "128x128"),
    (256, "128x128@2x"),
    (256, "256x256"),
    (512, "256x256@2x"),
    (512, "512x512"),
    (1024, "512x512@2x"),
]


def _corner_bg(im: Image.Image) -> tuple[int, int, int]:
    px = im.load()
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    rs = [px[x, y][0] for x, y in pts]
    gs = [px[x, y][1] for x, y in pts]
    bs = [px[x, y][2] for x, y in pts]
    return int(sum(rs) / 4), int(sum(gs) / 4), int(sum(bs) / 4)


def _corners_transparent(im: Image.Image, threshold: int = 32) -> bool:
    alpha = im.convert("RGBA").split()[-1]
    w, h = alpha.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    return all(alpha.getpixel(p) <= threshold for p in pts)


def remove_dark_background(im: Image.Image, tolerance: int = 48, softness: int = 42) -> Image.Image:
    """Soft chroma-key from corner background — for icons that still have a solid backdrop."""
    out = im.convert("RGBA")
    bg = _corner_bg(out)
    px = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            diff = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            if diff <= tolerance:
                px[x, y] = (r, g, b, 0)
            elif diff <= tolerance + softness:
                t = (diff - tolerance) / max(softness, 1)
                px[x, y] = (r, g, b, int(255 * t))
    return out


def trim_transparent(im: Image.Image, pad_ratio: float = 0.04) -> Image.Image:
    alpha = im.split()[-1]
    box = alpha.getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    pad = max(2, int(max(x1 - x0, y1 - y0) * pad_ratio))
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))


def pad_to_square(im: Image.Image) -> Image.Image:
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return canvas


def prepare_source(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    if _corners_transparent(im):
        return pad_to_square(trim_transparent(im))
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    return pad_to_square(trim_transparent(remove_dark_background(im)))


def build_icns(master: Image.Image) -> None:
    if sys.platform != "darwin":
        print("Skipping .icns (run on macOS to build CheckItNow.icns)")
        return
    iconset = ROOT / "CheckItNow.iconset"
    if iconset.exists():
        shutil.rmtree(iconset)
    iconset.mkdir()
    for size, name in ICNS_SPECS:
        master.resize((size, size), Image.Resampling.LANCZOS).save(
            iconset / f"icon_{name}.png"
        )
    subprocess.run(
        ["iconutil", "-c", "icns", str(iconset), "-o", str(ICNS)],
        check=True,
    )
    shutil.rmtree(iconset)
    print(f"Wrote {ICNS.name}")


def resolve_source() -> Path:
    for candidate in (SRC, LOGO, ICO):
        if candidate.exists():
            return candidate
    raise SystemExit(
        f"Missing icon source — add one of: {SRC.name}, {LOGO.name}, {ICO.name}"
    )


def build_icon() -> None:
    source = resolve_source()
    img = prepare_source(Image.open(source))
    layers = [img.resize((s, s), Image.Resampling.LANCZOS) for s in SIZES]
    LOGO.parent.mkdir(parents=True, exist_ok=True)
    layers[0].save(ICO, format="ICO", sizes=[(s, s) for s in SIZES])
    layers[0].save(LOGO)
    print(f"Wrote {ICO.name} + {LOGO.relative_to(ROOT)}")
    master = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    build_icns(master)


if __name__ == "__main__":
    build_icon()
