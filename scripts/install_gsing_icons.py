#!/usr/bin/env python3
"""Install user-provided 512px Gsing normal/dark icons into the AppIcon catalog.

Run from a checkout of the private Gsing source:
    python3 scripts/install_gsing_icons.py /path/to/gsing.png /path/to/gsingdark.png

The script changes only the app-icon asset catalog. It does NOT build an IPA.
Requires Pillow and SciPy (pip install pillow scipy numpy).
"""
from pathlib import Path
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt

CATALOG = (
    Path(__file__).resolve().parents[1]
    / "Gsing/Resources/Assets.xcassets/AppIcon.appiconset"
)


def prepare_icon(source: Path, target: Path) -> None:
    image = Image.open(source).convert("RGB")
    if image.size != (512, 512):
        raise ValueError(f"{source.name}: expected exactly 512 x 512 pixels")

    scale = 4
    mask = Image.new("L", (512 * scale, 512 * scale), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (2 * scale, 2 * scale, 510 * scale - 1, 510 * scale - 1),
        radius=131 * scale,
        fill=255,
    )
    mask = mask.resize((512, 512), Image.Resampling.LANCZOS)
    inside = np.asarray(mask) > 250

    # Apple's AppIcon catalog should use an opaque, square image and let iOS
    # do the corner rounding. Refill only the black matte at the very corners.
    # Preserve the provided image exactly within the rounded-square region.
    interior = Image.new("L", (512, 512), 0)
    ImageDraw.Draw(interior).rounded_rectangle(
        (19, 19, 492, 492), radius=116, fill=255
    )
    source_region = np.asarray(interior) > 0
    _, nearest = distance_transform_edt(
        ~source_region, return_indices=True
    )
    rgb = np.asarray(image)
    filled = rgb[tuple(nearest)]
    output = np.where(inside[..., None], rgb, filled).astype(np.uint8)
    target.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(output, "RGB").save(target, optimize=True)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: install_gsing_icons.py gsing.png gsingdark.png"
        )
    prepare_icon(Path(sys.argv[1]), CATALOG / "Gsing-default.png")
    prepare_icon(Path(sys.argv[2]), CATALOG / "Gsing-dark.png")

    contents_path = CATALOG / "Contents.json"
    obj = json.loads(contents_path.read_text())
    for entry in obj["images"]:
        appearances = entry.get("appearances", [])
        if any(
            x.get("value") in ("dark", "tinted")
            for x in appearances
        ):
            entry["filename"] = "Gsing-dark.png"
        elif entry.get("idiom") == "universal":
            entry["filename"] = "Gsing-default.png"

    contents_path.write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    )
    print("Normal and Dark icons installed at 512 x 512.")
    print("Original central content preserved; black corner matte removed.")
    print("No IPA build has been run.")


if __name__ == "__main__":
    main()
