# Capy's Last.fm Almanac, v1 build kit

Live dashboard: https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB

To refresh:
1. Run `bash fetch.sh`. It pulls data/scrobbles.csv and lastfm_cache/leaderboard_history.json from github.com/troycapybara2/scrobblemaxxing, rebuilds df_raw.pkl and puts art3.json in /tmp. (Older step-by-step notes below still describe what it does.)
2. Rebuild df_raw.pkl from it (uts > 1e9, ts in America/New_York), then run: bash refresh_all.sh
3. Upload every changed CSV in out/ to the artifact and point each dataset at its new file.

Your judgment lives in these files:
- buckets6.py: the 25 lanes (B) and the notes inside them (SUB), plus the "with the trop" artist set
- playlist.py: the shared "driving with the trop" playlist
- life.py / life_build.py: life chapters, work and school periods, milestones
- screams_build.py: core and some-screams tiers
- emo_build.py: waves and feels for the pop punk to emo map
- solar_positions.json: last galaxy layout, so the map stays stable between refreshes
- page/: the dashboard's HTML and JS

Fresh-chat refresh (cheapest way to run it):
1. Start a new chat and upload this zip.
2. Say: "Unzip the almanac build kit, run bash fetch.sh then bash refresh_all.sh, and update the artifact https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB. Compare every rebuilt file to the live one and upload only what changed."
