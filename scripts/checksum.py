#!/usr/bin/env python3
"""Compute a SHA-256 checksum for a file."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute SHA-256 for a file.")
    parser.add_argument("file", type=Path, help="Path to the file to hash")
    args = parser.parse_args()

    if not args.file.is_file():
        parser.error(f"not a file: {args.file}")

    print(f"{sha256_file(args.file)}  {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
