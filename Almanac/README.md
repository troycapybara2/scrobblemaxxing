# Capy's Last.fm Almanac, build kit (lives in the Almanac folder of troycapybara2/scrobblemaxxing)

Live dashboard: https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB

To refresh (one upload, one commit):
1. Pull this Almanac folder from the repo, then run `bash fetch.sh`. It pins to the newest commit, pulls data/scrobbles.csv and lastfm_cache/leaderboard_history.json, rebuilds df_raw.pkl and puts art3.json in /tmp.
2. Run `bash refresh_all.sh`. Its last step, bundle_build.py, packs every out/*.csv into out/bundle.json.
3. Upload out/bundle.json as an asset to the artifact, then update datasets/bundle in one write: source.url to the new /_blob/ url and updated.at to the current time (check the clock, don't guess).
4. Album covers are separate (datasets/album_art). Only if art_merged.json changed, upload it the same way and update datasets/album_art.

How the page reads data: datasets/bundle is the only data file besides album_art. page/bundle.js (files/bundle.js on the artifact) registers one dash.calc per dataset id that unpacks its slice of the bundle, so charts and data-source marks keep using the usual ids. A new CSV in out/ needs its own dash.calc line in bundle.js before the page can see it.

Your judgment lives in these files:
- buckets6.py: the 25 lanes (B) and the notes inside them (SUB), plus the "with the trop" artist set
- playlist.py: the shared "driving with the trop" playlist
- life.py / life_build.py: life chapters, work and school periods, milestones
- screams_build.py: core and some-screams tiers
- emo_build.py: waves and feels for the pop punk to emo map
- solar_positions.json: last galaxy layout, so the map stays stable between refreshes
- page/: the dashboard's HTML and JS

Fresh-chat refresh: start a new chat and say "Pull the Almanac folder from troycapybara2/scrobblemaxxing, run fetch.sh then refresh_all.sh, and update the artifact https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB by uploading the new bundle." No zip needed.
