#!/usr/bin/env python3
"""Fill in a `cover` thumbnail URL for each album in src/_data/albums.json.

Looks up each album's Discogs master/release via the public API and stores
its primary image's 150px thumbnail. An album can set `coverFrom` to another
Discogs master/release URL to take its cover from there instead (e.g. to pick
a particular pressing's artwork). Albums that already have a cover are
skipped unless --all is passed (use that if Discogs image links stop working).

    python3 scripts/fetch_covers.py [--all]
"""

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ALBUMS = Path(__file__).resolve().parent.parent / "src" / "_data" / "albums.json"
USER_AGENT = "mdsharpe-web/1.0 +https://www.mdsharpe.com/"
DELAY = 2.5  # unauthenticated API limit is 25 requests per minute


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def cover_for(discogs_url):
    match = re.search(r"/(master|release)/(\d+)", discogs_url)
    if not match:
        raise ValueError(f"Not a Discogs master/release URL: {discogs_url}")
    kind, id = match.groups()
    images = fetch(f"https://api.discogs.com/{kind}s/{id}").get("images") or []
    primary = next((i for i in images if i["type"] == "primary"), images[0] if images else None)
    return primary["uri150"] if primary else None


def main():
    refresh_all = "--all" in sys.argv[1:]
    albums = json.loads(ALBUMS.read_text(encoding="utf-8"))
    todo = [a for a in albums if refresh_all or not a.get("cover")]

    for n, album in enumerate(todo, 1):
        label = f"{album['artist']} - {album['title']}"
        try:
            cover = cover_for(album.get("coverFrom") or album["discogs"])
        except Exception as error:
            print(f"[{n}/{len(todo)}] FAILED {label}: {error}")
        else:
            if cover:
                album["cover"] = cover
            print(f"[{n}/{len(todo)}] {'ok' if cover else 'no image'} {label}")
        # Save as we go so an interrupted run keeps its progress.
        ALBUMS.write_text(json.dumps(albums, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        if n < len(todo):
            time.sleep(DELAY)


if __name__ == "__main__":
    main()
