"""
Twice-daily Last.fm snapshot for scrobblemaxxing, run by GitHub Actions.

1. Leaderboard: pulls the top 500 and appends one line to
   lastfm_cache/leaderboard_history_actions.json with only the artists whose
   play count or rank changed since the last run. Same line format the app
   uses ({"timestamp", "data"}), plus "source": "actions". It writes to its own
   file so it never collides with the app's saves to leaderboard_history.json.
2. Scrobbles: appends every new scrobble to data/scrobbles.csv, same columns as
   the Last.fm export. The first run backfills the whole history (takes a while).

Artist names are stored exactly as Last.fm returns them.
"""
import csv
import json
import os
import time
from datetime import datetime, timezone

import requests

USER = os.environ.get("LASTFM_USER", "troycapybara")
API_KEY = os.environ["LASTFM_API_KEY"]
API = "https://ws.audioscrobbler.com/2.0/"

HISTORY = "lastfm_cache/leaderboard_history_actions.json"
STATE = "lastfm_cache/actions_last_top500.json"
SCROBBLES = "data/scrobbles.csv"
COLS = ["uts", "utc_time", "artist", "artist_mbid", "album", "album_mbid", "track", "track_mbid"]


def call(**params):
    last = None
    for attempt in range(5):
        try:
            r = requests.get(API, params={"api_key": API_KEY, "format": "json", **params}, timeout=30)
            last = f"{r.status_code} {r.text[:200]}"
            if r.status_code == 200:
                data = r.json()
                if "error" not in data:
                    return data
        except requests.RequestException as e:
            last = str(e)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Last.fm {params.get('method')} failed: {last}")


def snapshot():
    artists = call(method="user.gettopartists", user=USER, period="overall", limit=500)["topartists"]["artist"]
    if len(artists) < 450:  # don't record a half-empty response
        raise RuntimeError(f"Only got {len(artists)} artists back; skipping this run")
    now = {a["name"]: {"playcount": int(a["playcount"]), "rank": i + 1} for i, a in enumerate(artists)}

    prev = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            prev = json.load(f)
    changed = {name: v for name, v in now.items() if prev.get(name) != v}

    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    if changed:
        line = {
            # naive UTC, matching the timestamps the Streamlit Cloud app writes
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec="milliseconds"),
            "data": changed,
            "source": "actions",
        }
        with open(HISTORY, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(now, f, ensure_ascii=False)
    print(f"Leaderboard: {len(changed)} artists changed")


def scrobbles():
    latest = 0
    if os.path.exists(SCROBBLES):
        with open(SCROBBLES, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                latest = max(latest, int(row["uts"]))

    rows, seen, page, pages = [], set(), 1, 1
    while page <= pages:
        params = {"method": "user.getrecenttracks", "user": USER, "limit": 200, "page": page}
        if latest:
            params["from"] = latest + 1
        rt = call(**params)["recenttracks"]
        pages = int(rt["@attr"]["totalPages"])
        tracks = rt.get("track", [])
        if isinstance(tracks, dict):  # Last.fm returns a dict when there's only one
            tracks = [tracks]
        for t in tracks:
            if t.get("@attr", {}).get("nowplaying") == "true" or "date" not in t:
                continue
            key = (t["date"]["uts"], t["artist"]["#text"], t["name"])
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "uts": int(t["date"]["uts"]), "utc_time": t["date"]["#text"],
                "artist": t["artist"]["#text"], "artist_mbid": t["artist"].get("mbid", ""),
                "album": t["album"]["#text"], "album_mbid": t["album"].get("mbid", ""),
                "track": t["name"], "track_mbid": t.get("mbid", ""),
            })
        page += 1
        time.sleep(0.25)

    rows.sort(key=lambda r: r["uts"])
    new_file = not os.path.exists(SCROBBLES)
    os.makedirs(os.path.dirname(SCROBBLES), exist_ok=True)
    with open(SCROBBLES, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new_file:
            w.writeheader()
        w.writerows(rows)
    print(f"Scrobbles: {len(rows)} new")


if __name__ == "__main__":
    snapshot()
    scrobbles()
