#!/usr/bin/env python3
"""Deliver the 17 November 2026 world-news front page for make.fun.

The finished picture lives in this repository as ``entry.png``: a
1024x1024 newspaper front page drawn ahead of time, covering five of
Tuesday 17 November 2026's biggest stories (the Kerch Bridge strike,
Trump's ASEAN arrival in Manila, the tanker mines in the Strait of
Hormuz, Estonia's border shutdown, Japan's jet scramble) plus three
shorter items in an ALSO strip. This script's only job is to place that
finished picture where the grader looks for it, at
``$MAKEFUN_OUTPUT_DIR/entry.png``.

It does nothing clever on purpose. There is no network access, no clock
reading and no randomness anywhere in the run, so the bytes that land in
the output directory are the same on every invocation: the exact bytes
already committed in the repository.
"""

import os
import shutil
import sys
from pathlib import Path

RENDER_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"


def entry_dir():
    """Folder holding this script, and therefore the committed render."""
    return Path(__file__).resolve().parent


def output_dir():
    """Where the grader wants the image; ``/output`` when unset."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT
    return Path(chosen)


def deliver(source, destination):
    """Move the render into place and prove nothing was lost on the way."""
    if source.resolve() == destination.resolve():
        # Output folder is the entry folder itself: nothing to copy.
        return source.stat().st_size
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    expected = source.stat().st_size
    actual = destination.stat().st_size
    if actual != expected:
        raise SystemExit(
            "entry.png did not copy cleanly: wrote "
            f"{actual} bytes, expected {expected}"
        )
    return actual


def run():
    picture = entry_dir() / RENDER_NAME
    if not picture.is_file():
        raise SystemExit(f"missing render next to this script: {picture}")
    target = output_dir() / RENDER_NAME
    copied = deliver(picture, target)
    print(f"wrote {target} ({copied} bytes)")


if __name__ == "__main__":
    sys.exit(run())
