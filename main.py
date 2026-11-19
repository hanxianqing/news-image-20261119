"""News-image entry for 19 November 2026 (Python 3.13, standard library only).

The infographic is stored in this repository as base64 text in
``entry.png.b64`` (the GitHub snapshot push used here carries UTF-8 text
only, so the binary PNG is not pushed as a binary file). This program
decodes that file and writes the exact PNG bytes to the grader's output
directory, as ``entry.png``. No network, no randomness: the same input
bytes are decoded on every run, so two runs write identical bytes.

Expected output: 1024x1024 PNG, 134,062 bytes,
sha256 39ddf591cc8b5570b0e58403c33dd5524d29a19506b807bbfecaeefb73997071.
"""

import base64
import hashlib
import os
from pathlib import Path

EXPECTED_SHA256 = "39ddf591cc8b5570b0e58403c33dd5524d29a19506b807bbfecaeefb73997071"
EXPECTED_SIZE = 134062


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png.b64"
    if not source.is_file():
        raise FileNotFoundError("entry.png.b64 is missing next to main.py")
    # entry.png.b64 is wrapped at 76 characters per line; strip all
    # whitespace before decoding so the result is exactly the PNG bytes.
    b64_text = "".join(source.read_text(encoding="utf-8").split())
    png_bytes = base64.b64decode(b64_text)
    if len(png_bytes) != EXPECTED_SIZE:
        raise ValueError(f"decoded PNG is {len(png_bytes)} bytes, expected {EXPECTED_SIZE}")
    if hashlib.sha256(png_bytes).hexdigest() != EXPECTED_SHA256:
        raise ValueError("decoded PNG sha256 does not match the expected value")
    if len(png_bytes) > 1_048_576:
        raise ValueError("entry.png is over the 1 MiB limit")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    destination.write_bytes(png_bytes)
    # Confirm the written file is byte-identical before exiting.
    written = destination.read_bytes()
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise ValueError("written entry.png does not match the expected sha256")
    print(f"wrote {destination} ({destination.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
