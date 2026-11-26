#!/usr/bin/env python3
"""Entry point for the news-image-20261125 competition.

Copies the pre-rendered entry.png (drawn by render.py, which lives in
this repository) into the output directory the grader provides. Standard
library only: no image library is imported, so it runs in the grader's
bare Python environment.

The output directory comes from MAKEFUN_OUTPUT_DIR, defaulting to
/output. The copy is byte-for-byte, so repeated runs are identical.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
