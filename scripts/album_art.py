"""
Album art thumbnails for the Last.fm almanac, run by GitHub Actions.

Pulls your top 500 albums from Last.fm, shrinks each cover to a small JPEG,
and stores them in data/album_art.json as {"Artist || Album": "data:image/jpeg;base64,..."}.
Only albums it hasn't seen before get downloaded, so after the first run
this takes a few seconds. Names are kept exactly as Last.fm returns them.
"""
import base64
import io
import json
import os
import time

import requests
from PIL import Image

USER = os.environ.get("LASTFM_USER", "troycapybara")
API_KEY = os.environ["LASTFM_API_KEY"]
API = "https://ws.audioscrobbler.com/2.0/"
OUT = "data/album_art.json"
LIMIT = 1250
SIZE = 120  # pixels on the long side
PLACEHOLDER = "2a96cbd8b46e442fc41c2b86b821562f"  # Last.fm's blank star image


def call(**params):
    last = None
    for attempt in range(5):
        try:
            r = requests.get(API, params={"api_key": API_KEY, "format": "json", **params}, timeout=30)
            last = f"{r.status_code} {r.text[:200]}"
            if r.status_code == 200 and "error" not in r.json():
                return r.json()
        except requests.RequestException as e:
            last = str(e)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Last.fm {params.get('method')} failed: {last}")


def main():
    art = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            art = json.load(f)

    albums = call(method="user.gettopalbums", user=USER, period="overall", limit=LIMIT)["topalbums"]["album"]
    added = 0
    for a in albums:
        key = f'{a["artist"]["name"]} || {a["name"]}'
        if key in art:
            continue
        url = next((i["#text"] for i in reversed(a.get("image", [])) if i.get("#text")), "")
        if not url or PLACEHOLDER in url:
            art[key] = ""  # no cover on Last.fm; remembered so it isn't retried every run
            continue
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            im = Image.open(io.BytesIO(r.content)).convert("RGB")
            im.thumbnail((SIZE, SIZE))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=72, optimize=True)
            art[key] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
            added += 1
        except Exception as e:  # one bad image shouldn't stop the rest
            print(f"Skipped {key}: {e}")
        time.sleep(0.1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(art, f, ensure_ascii=False)
    print(f"Album art: {added} new covers, {sum(1 for v in art.values() if v)} total")


if __name__ == "__main__":
    main()
