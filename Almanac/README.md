# Capy's Last.fm Almanac, build kit (lives in the Almanac folder of troycapybara2/scrobblemaxxing)

Live dashboard: https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB

To refresh (one upload, one commit):
1. Pull this Almanac folder from the repo, then run `bash fetch.sh`. It pins to the newest commit, pulls data/scrobbles.csv and lastfm_cache/leaderboard_history.json, rebuilds df_raw.pkl and puts art3.json in /tmp.
2. Pull Capy's own lane tags: with the Artifact tool, read_db on the artifact, collection `data/users/me`, doc `lf-tags`. Save its data as my_tags.json in this folder ({"tags": [{"artist", "lane", "at"}, ...]}). If there's no such doc, skip this. buckets6.py applies these tags over its own lists, and they always win. Do the same for doc `lf-strays` (his Keep it coming / Not a stray votes on the strays shelf), saved as my_strays.json ({"items": [{"artist", "track", "vote", "at"}, ...]}); strays_build.py drops Not a stray songs and boosts kept ones. Mention any newly applied tags or votes in the reply.
3. Run `bash refresh_all.sh`. Its last step, bundle_build.py, packs every out/*.csv into out/bundle.json.
4. Upload out/bundle.json as an asset to the artifact, then update datasets/bundle in one write: source.url to the new /_blob/ url and updated.at to the current time (check the clock, don't guess).
5. Album covers are separate (datasets/album_art). Only if art_merged.json changed, upload it the same way and update datasets/album_art.

How the page reads data: datasets/bundle is the only data file besides album_art. page/bundle.js (files/bundle.js on the artifact) registers one dash.calc per dataset id that unpacks its slice of the bundle, so charts and data-source marks keep using the usual ids. A new CSV in out/ needs its own dash.calc line in bundle.js before the page can see it.

Your judgment lives in these files:
- buckets6.py: the 25 lanes (B) and the notes inside them (SUB), plus the "with the trop" artist set. Tags Capy saves from artist cards in the almanac (my_tags.json) override B.
- playlist.py: the shared "driving with the trop" playlist
- life.py / life_build.py: life chapters, work and school periods, milestones
- screams_build.py: core and some-screams tiers
- emo_build.py: waves and feels for the pop punk to emo map
- strays_build.py: the rule for the strays shelf (outside the lanes, at least half the artist's plays, 3+ visits 60+ days apart)
- solar_positions.json: last galaxy layout, so the map stays stable between refreshes
- page/: the dashboard's HTML and JS

Fresh-chat refresh: start a new chat and say "Pull the Almanac folder from troycapybara2/scrobblemaxxing and follow its README to refresh https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB." No zip needed.
