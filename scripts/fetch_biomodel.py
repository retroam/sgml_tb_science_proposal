#!/usr/bin/env python3
"""Best-effort fetcher for BioModels BIOMD0000000151 SBML."""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL_ID = "BIOMD0000000151"
OUTPUT = Path("source") / f"{MODEL_ID}.xml"
URLS = [
    "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000151.3?filename=BIOMD0000000151_url.xml",
    "https://www.biomodels.org/model/download/BIOMD0000000151.3?filename=BIOMD0000000151_url.xml",
    "https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000151?filename=BIOMD0000000151_url.xml",
    "https://www.biomodels.org/model/download/BIOMD0000000151?filename=BIOMD0000000151_url.xml",
    "https://www.ebi.ac.uk/biomodels/BIOMD0000000151/download?filename=BIOMD0000000151_url.xml",
    "https://www.ebi.ac.uk/biomodels/model/files/BIOMD0000000151/BIOMD0000000151_url.xml",
    "https://www.ebi.ac.uk/biomodels/model/files/BIOMD0000000151/BIOMD0000000151.xml",
]


def looks_like_sbml(data: bytes) -> bool:
    sample = data[:4096].lower()
    return b"<sbml" in sample or (b"<?xml" in sample and b"sbml" in sample)


def fetch(url: str) -> tuple[int | str, bytes]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 sbml-netflux-proposal-fetch/1.0",
            "Accept": "application/xml,text/xml,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.getcode()
            data = response.read(20 * 1024 * 1024)
            return status, data
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(4096)
    except urllib.error.URLError as exc:
        return f"ERROR {exc.reason}", b""


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    for url in URLS:
        status, data = fetch(url)
        print(f"{status} {url}")
        if isinstance(status, int) and 200 <= status < 300 and looks_like_sbml(data):
            OUTPUT.write_bytes(data)
            print(f"saved {OUTPUT} ({len(data)} bytes)")
            return 0
        if data:
            preview = data[:120].replace(b"\n", b" ").replace(b"\r", b" ")
            print(f"  response did not look like SBML: {preview!r}")
    print("No SBML-looking response found. Use the BioModels UI manually and do not invent a checksum.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
