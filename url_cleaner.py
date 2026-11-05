#!/usr/bin/env python3
"""Strip tracking parameters from URLs.

Removes common tracking query parameters (utm_*, fbclid, gclid, and
friends) while keeping everything else -- path, kept parameters, and
fragment -- untouched. Reads URLs from the command line, or one per
line from stdin when no arguments are given.

Stdlib only. Nothing leaves your machine.
"""

import argparse
import sys
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# Parameters that only exist to track you. utm_* is matched by prefix;
# the rest are matched exactly (case-insensitive).
TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "gbraid",
    "wbraid",
    "msclkid",
    "mc_cid",
    "mc_eid",
    "igshid",
    "twclid",
    "srsltid",
    "vero_id",
    "_ga",
    "_gl",
    "dclid",
    "yclid",
    "scid",
}


def is_tracking(name, keep):
    """True if a query parameter is a tracker and not explicitly kept."""
    lowered = name.lower()
    if lowered in keep:
        return False
    if lowered.startswith("utm_"):
        return True
    return lowered in TRACKING_PARAMS


def clean_url(url, keep=frozenset()):
    """Return (cleaned_url, removed_params) for one URL.

    Raises ValueError if the URL has no http(s) scheme or no host.
    """
    parsed = urlparse(url.strip())
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"not a valid http(s) URL: {url!r}")
    kept = []
    removed = []
    for name, value in parse_qsl(parsed.query, keep_blank_values=True):
        if is_tracking(name, keep):
            removed.append(name)
        else:
            kept.append((name, value))
    cleaned = urlunparse(parsed._replace(query=urlencode(kept)))
    return cleaned, removed


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Strip tracking parameters from URLs."
    )
    parser.add_argument("urls", nargs="*", help="URLs to clean (default: stdin)")
    parser.add_argument(
        "--keep",
        default="",
        help="comma-separated parameters to keep even if they look like trackers",
    )
    parser.add_argument(
        "--show-removed",
        action="store_true",
        help="print removed parameter names to stderr, one line per URL",
    )
    args = parser.parse_args(argv)

    keep = {name.strip().lower() for name in args.keep.split(",") if name.strip()}
    if args.urls:
        lines = args.urls
    else:
        lines = [line.strip() for line in sys.stdin if line.strip()]
        if not lines:
            parser.error("no URLs given (pass arguments or pipe URLs on stdin)")

    failed = False
    for line in lines:
        try:
            cleaned, removed = clean_url(line, keep)
        except ValueError as exc:
            print(f"url_cleaner: {exc}", file=sys.stderr)
            failed = True
            continue
        print(cleaned)
        if args.show_removed:
            print(f"removed: {', '.join(removed) or '(none)'}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
