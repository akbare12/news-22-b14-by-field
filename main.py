#!/usr/bin/env python3
"""news-22 b14 by-field entrypoint: copy entry.png to the grader output dir.

The grader runs this program twice in a sandbox with a read-only /bot and a
writable /output. It must never write next to itself: the destination is
always os.environ["MAKEFUN_OUTPUT_DIR"] (default "out" for local runs).
"""
import hashlib
import os
import shutil
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    # Stdlib-only check: PNG magic + IHDR width/height (no PIL in the sandbox).
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        print("not a PNG", file=sys.stderr)
        return 1
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        print("bad size", (w, h), file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        got = hashlib.sha256(f.read()).hexdigest()
    if got != hashlib.sha256(data).hexdigest():
        print("sha256 mismatch", file=sys.stderr)
        return 1
    print("OK", dst, got)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
