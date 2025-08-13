# shrink_in_place.py
from pathlib import Path
from PIL import Image

MEDIA_DIR = Path("media/products")
MAX_WIDTH = 1200
QUALITY = 82

def optimize_image(path):
    try:
        img = Image.open(path)
    except Exception:
        return
    img = img.convert("RGB") if img.mode not in ("RGB", "L") else img
    w, h = img.size
    if w > MAX_WIDTH:
        ratio = MAX_WIDTH / w
        img = img.resize((MAX_WIDTH, int(h * ratio)), Image.Resampling.LANCZOS)
    img.save(path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"Optimized {path}")

for file in MEDIA_DIR.rglob("*"):
    if file.suffix.lower() in [".jpg", ".jpeg"]:
        optimize_image(file)
