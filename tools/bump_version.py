#!/usr/bin/env python3
"""Bump the pre-release version in src/cchardet/__init__.py.

Reads __version__ (e.g. "2.2.0a3"), increments the alpha segment,
updates both the version tuple and the __version__ string, and writes
the new version to $GITHUB_OUTPUT (version=, tag=).

Usage:
    python tools/bump_version.py
"""
import os
import re
import sys
from pathlib import Path

INIT = Path("src/cchardet/__init__.py")


def main():
    text = INIT.read_text()

    ver_match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)a(\d+)"', text)
    if not ver_match:
        print("ERROR: cannot parse __version__ (expected format: X.Y.ZaN)", file=sys.stderr)
        sys.exit(1)

    major, minor, patch, alpha = ver_match.groups()
    new_alpha = int(alpha) + 1
    new_version = f"{major}.{minor}.{patch}a{new_alpha}"

    text = re.sub(
        r'__version__\s*=\s*"[^"]*"',
        f'__version__ = "{new_version}"',
        text,
    )
    text = re.sub(
        r'version\s*=\s*\(\d+,\s*\d+,\s*\d+,\s*"alpha",\s*\d+\)',
        f'version = ({major}, {minor}, {patch}, "alpha", {new_alpha})',
        text,
    )

    INIT.write_text(text)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"version={new_version}\n")
            f.write(f"tag=v{new_version}\n")

    print(f"Bumped: {ver_match.group(0)} -> {new_version}")


if __name__ == "__main__":
    main()
