"""Build every Capybara Cartel logo variant from the one source image.

Run from anywhere:  python tools/make_logos.py
Source: brand/source/capybara-cartel-logo-original.jpg (cream art on rust brown, 1024x1024)
Output: brand/  (press-kit files) and assets/img/  (small files the website uses)

The art is cream on a flat brown field, so the cream's brightness becomes the alpha
channel. That lets us repaint the same art in any colour on any background.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand" / "source" / "capybara-cartel-logo-original.jpg"
BRAND = ROOT / "brand"
WEB = ROOT / "assets" / "img"

# Brand colours (sampled from the logo)
RUST = (135, 70, 30)      # #87461E  the background
CREAM = (238, 228, 203)   # #EEE4CB  the art
INK = (43, 26, 14)        # #2B1A0E  dark ink for light backgrounds
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Where the art sits in the 1024 source (measured: a 3-row gap at y=756-758
# separates the head from the name plate).
HEAD_Y = (100, 756)
PLATE_Y = (759, 924)


def alpha_from_source(img: Image.Image) -> np.ndarray:
    """0..1 coverage of the cream art, from luminance."""
    lum = np.asarray(img.convert("L"), dtype=np.float32)
    lo, hi = 94.0, 220.0          # background sits at ~85, cream at ~227
    a = np.clip((lum - lo) / (hi - lo), 0.0, 1.0)
    return a


def paint(alpha: np.ndarray, colour, background=None) -> Image.Image:
    """Art in `colour`, on transparent (background=None) or on a solid colour."""
    h, w = alpha.shape
    if background is None:
        out = np.zeros((h, w, 4), dtype=np.uint8)
        out[..., :3] = colour
        out[..., 3] = np.round(alpha * 255).astype(np.uint8)
        return Image.fromarray(out, "RGBA")
    a = alpha[..., None]
    rgb = np.array(background, np.float32) * (1 - a) + np.array(colour, np.float32) * a
    return Image.fromarray(np.round(rgb).astype(np.uint8), "RGB")


def bbox(alpha: np.ndarray, thresh=0.12):
    ys, xs = np.where(alpha > thresh)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def crop(alpha: np.ndarray, y_range, pad=0):
    # Blank everything outside the band first, so padding never pulls in a
    # sliver of the neighbouring piece (the beard tip, the plate's top edge).
    masked = np.zeros_like(alpha)
    masked[y_range[0]:y_range[1], :] = alpha[y_range[0]:y_range[1], :]
    x0, y0, x1, y1 = bbox(masked)
    h, w = alpha.shape
    return masked[max(0, y0 - pad):min(h, y1 + pad), max(0, x0 - pad):min(w, x1 + pad)]


def square(alpha: np.ndarray, margin=0.12) -> np.ndarray:
    """Centre the art on a square transparent canvas with `margin` on each side."""
    h, w = alpha.shape
    side = int(max(h, w) / (1 - 2 * margin))
    out = np.zeros((side, side), np.float32)
    oy, ox = (side - h) // 2, (side - w) // 2
    out[oy:oy + h, ox:ox + w] = alpha
    return out


def resize(alpha: np.ndarray, width=None, height=None) -> np.ndarray:
    h, w = alpha.shape
    if width:
        height = round(h * width / w)
    elif height:
        width = round(w * height / h)
    im = Image.fromarray(np.round(alpha * 255).astype(np.uint8), "L")
    im = im.resize((width, height), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255.0


def save(img: Image.Image, path: Path, **kw):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True, **kw)
    print(f"  {path.relative_to(ROOT)}  {img.size[0]}x{img.size[1]}")


def variant_set(name: str, alpha: np.ndarray, folder: Path):
    """The six treatments every logo piece comes in."""
    save(paint(alpha, CREAM, RUST), folder / f"{name}-rust.png")                 # the original look
    save(paint(alpha, RUST, CREAM), folder / f"{name}-cream.png")                # light badge
    save(paint(alpha, CREAM), folder / f"{name}-cream-transparent.png")          # on dark or photos
    save(paint(alpha, INK), folder / f"{name}-ink-transparent.png")              # on light or paper
    save(paint(alpha, BLACK), folder / f"{name}-black-transparent.png")          # print, stamps, laser
    save(paint(alpha, WHITE), folder / f"{name}-white-transparent.png")          # dark photos, video


def main():
    src = Image.open(SRC).convert("RGB")
    full = alpha_from_source(src)

    lockup = crop(full, (HEAD_Y[0], PLATE_Y[1]), pad=24)
    head = crop(full, HEAD_Y, pad=16)
    plate = crop(full, PLATE_Y, pad=12)

    print("Press kit (brand/):")
    variant_set("capybara-cartel-lockup", lockup, BRAND / "lockup")
    variant_set("capybara-cartel-mark", head, BRAND / "mark")
    variant_set("capybara-cartel-wordmark", plate, BRAND / "wordmark")

    # Square versions of the original full-square logo and the mark
    save(paint(square(lockup, 0.08), CREAM, RUST), BRAND / "lockup" / "capybara-cartel-lockup-square-rust.png")
    mark_sq = square(head, 0.10)
    save(paint(mark_sq, CREAM, RUST), BRAND / "mark" / "capybara-cartel-mark-square-rust.png")

    # Profile picture: platforms crop to a circle, so keep the art inside the middle ~70%
    avatar = resize(square(head, 0.17), width=800)
    save(paint(avatar, CREAM, RUST), BRAND / "social" / "capybara-cartel-avatar-800.png")

    # Banner / Open Graph card 1200x630 (what shows when the site link is shared)
    og = Image.new("RGB", (1200, 630), RUST)
    art = resize(lockup, height=560)
    og.paste(paint(art, CREAM, RUST), ((1200 - art.shape[1]) // 2, 35))
    save(og, BRAND / "social" / "capybara-cartel-og-1200x630.png")

    # Wide banner for YouTube / X / itch headers (1500x500), mark left of the name plate
    banner = Image.new("RGB", (1500, 500), RUST)
    m = resize(head, height=400)
    p = resize(plate, width=780)
    gap = 60
    total = m.shape[1] + gap + p.shape[1]
    x0 = (1500 - total) // 2
    banner.paste(paint(m, CREAM, RUST), (x0, 50))
    banner.paste(paint(p, CREAM, RUST), (x0 + m.shape[1] + gap, (500 - p.shape[0]) // 2))
    save(banner, BRAND / "social" / "capybara-cartel-banner-1500x500.png")

    # App / browser icons: mark on rust, square
    icons = BRAND / "icons"
    for size in (512, 192, 180, 48, 32, 16):
        a = resize(square(head, 0.08 if size >= 48 else 0.02), width=size)
        save(paint(a, CREAM, RUST), icons / f"icon-{size}.png")
    # Maskable icon (Android trims up to 20% per side): extra margin
    save(paint(resize(square(head, 0.22), width=512), CREAM, RUST), icons / "icon-maskable-512.png")
    ico_src = paint(resize(square(head, 0.02), width=256), CREAM, RUST)
    ico_src.save(icons / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  brand/icons/favicon.ico  16/32/48")

    print("Website (assets/img/):")
    save(paint(resize(lockup, width=880), CREAM), WEB / "lockup-cream.png")
    save(paint(resize(head, height=112), CREAM), WEB / "mark-cream-112.png")
    save(paint(resize(head, height=220), INK), WEB / "mark-ink-220.png")
    save(paint(resize(plate, width=560), INK), WEB / "wordmark-ink-560.png")
    for name in ("favicon.ico", "icon-180.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "icon-32.png"):
        (WEB / name).write_bytes((icons / name).read_bytes())
    (WEB / "og-image.png").write_bytes((BRAND / "social" / "capybara-cartel-og-1200x630.png").read_bytes())
    print("Done.")


if __name__ == "__main__":
    main()
