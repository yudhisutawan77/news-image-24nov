#!/usr/bin/env python3
"""News image entry for 24 November 2026 (make.fun news-image-20261124).

The picture of the day's world news lives beside this file as entry.png
(a newspaper front page drawn for this competition: the Indonesia factory
fire, a Russian cargo ship ablaze after a drone strike, COP31 ending with
no fossil-fuel deal, Alcaraz winning the ATP Finals, and Nvidia's ~$1tn
rally). This program copies that image to /output/entry.png.

Standard library only, no network, deterministic: the same bytes are
written on every run. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DEST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    dest = os.path.join(DEST_DIR, "entry.png")
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    assert size <= 1048576, f"entry.png too large: {size} bytes"
    print(f"wrote {dest} ({size} bytes)")


if __name__ == "__main__":
    main()
