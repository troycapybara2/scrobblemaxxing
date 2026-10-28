# Capy's Command Center, build kit

Live page: https://claude.ai/artifact/ThdS17KsRxY63BYkrpbbGA

## What's here
- `picks.py`: the hand-picked crate albums (artist, album, year, lane, canon, anchors, why, home tag)
- `rym.py`, `rym2.py`: RYM all-time top 400 (ranks 1-78 and 79-400), with lane/genre clusters and write-ups
- `build.py`: matches every pick against `data/scrobbles.csv`, sets statuses, writes `data.json`
- `prep.py`: display formatting, scores and ids, writes `data2.json`
- `page.html`: the page template; `__DATA__` gets replaced with `data2.json` (plus the artist-to-lane map from `Almanac/artist_lanes.csv`)

## How the page works
- Snapshot counts come from `data/scrobbles.csv` at build time (`baseUts` = newest scrobble).
- Live plays come from the custom "Last.fm" connector (Worker in `CC/`, tool `recent_scrobbles`, since `baseUts`, up to 2,000 scrobbles). Refresh the snapshot before that runs out.
- Marks, ratings, discoveries, badges, weekly digs and the graduation shelf save to the artifact db at `data/users/<viewer>/disc-votes` (Claude reads it with read_db at `data/users/me`).
- Runtime capabilities: db, user, mcp (Last.fm: recent_scrobbles).

## Refreshing the snapshot
Run build.py, then prep.py, add the artist_lanes map to data2.json, inject into page.html, publish to the URL above. Stored discoveries keep their own starting counts, so they survive a refresh.
