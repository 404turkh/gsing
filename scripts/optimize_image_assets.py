#!/usr/bin/env python3
"""Losslessly recompress Gsing's source PNGs, without resizing or deleting assets.

This is an *asset-only* maintenance step, not an iOS/IPA build.
Every image's decoded RGBA pixels are verified before retaining changes.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "Gsing" / "Resources"


def fingerprint(path: Path) -> tuple[tuple[int, int], str]:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        return image.size, hashlib.sha256(rgba.tobytes()).hexdigest()


def main() -> None:
    count = 0
    total_before = 0
    total_after = 0
    for path in sorted(ROOT.rglob("*.png")):
        before = path.read_bytes()
        original_pixels = fingerprint(path)
        subprocess.run(
            ["optipng", "-o3", "-quiet", str(path)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        after = path.read_bytes()
        if fingerprint(path) != original_pixels:
            path.write_bytes(before)
            raise RuntimeError(f"Image pixels changed unexpectedly: {path}")
        if len(after) > len(before):
            path.write_bytes(before)
            after = before
        count += 1
        total_before += len(before)
        total_after += len(after)
        print(f"{path.relative_to(ROOT)}: {len(before):,} -> {len(after):,} bytes")

    print(f"Optimized {count} images: {total_before:,} -> {total_after:,} bytes")
    print(f"Space saved in source PNGs: {total_before - total_after:,} bytes")
    print("All RGBA pixels and dimensions were verified unchanged.")


if __name__ == "__main__":
    main()
