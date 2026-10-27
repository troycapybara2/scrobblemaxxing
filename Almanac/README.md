# Capy's Last.fm Almanac, build kit (lives in the Almanac folder of troycapybara2/scrobblemaxxing)

Live dashboard: https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB

To refresh (one upload, one commit):
1. Pull this Almanac folder from the repo, then run `bash fetch.sh`. It pins to the newest commit, pulls data/scrobbles.csv and lastfm_cache/leaderboard_history.json, rebuilds df_raw.pkl and puts art3.json in /tmp.
2. Pull Capy's own lane tags: with the Artifact tool, read_db on the artifact, collection `data/users/me`, doc `lf-tags`. Save its data as my_tags.json in this folder ({"tags": [{"artist", "lane", "at"}, ...]}). If there's no such doc, skip this. buckets6.py applies these tags over its own lists, and they always win. Do the same for doc `lf-strays` (his Keep it coming / Not a stray votes on the strays shelf), saved as my_strays.json ({"items": [{"artist", "track", "vote", "at"}, ...]}); strays_build.py drops Not a stray songs and boosts kept ones. And doc `lf-gone` (Bring it back / Gone for good votes on the Long gone shelf) as my_gone.json ({"items": [{"artist", "vote", "at"}, ...]}); gone_build.py drops Gone for good artists and boosts the rest. Also save doc `lf-categorize` (his categorizing-game answers) as my_categorize.json; sounds_build.py turns it into the "sounds like" links and the ears-vs-galaxy scorecard. Before uploading anything, read datasets/bundle on the artifact and write the date of its updated.at (YYYY-MM-DD) to last_refresh.txt; recent_build.py shows a "while you were away" recap when that was 14+ days before the latest scrobble. Mention any newly applied tags or votes in the reply.
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
- sounds_build.py: "sounds like" links (sound, scene, member) and the ears-vs-galaxy scorecard
- artist_places.csv + places_build.py: the artist map (hometowns; Capy's own answers with q = place in my_categorize.json override the list)
- arcs_build.py: artist arcs (the shape of each top artist's history; rules at the top of the file)
- next_build.py: what comes next (song-to-song steps and artist hops)
- power_build.py: power climbers and lane momentum (seats in the top 500 and median move per lane since launch) (climb as a rank ratio x sqrt of plays added since launch)
- drives_build.py: the Bloomfield to Morrisville drives (Capy's rule: start 2:30pm or later, 70+ minutes)
- gone_build.py: the Long gone shelf (50+ plays, nothing in 18 months)
- bridges_build.py: bridge artists between galaxy clusters
- sounds_build.py: "sounds like" links (sound, scene, member) and the ears-vs-galaxy scorecard
- artist_places.csv + places_build.py: the artist map (hometowns; Capy's own answers with q = place in my_categorize.json override the list)
- arcs_build.py: artist arcs (the shape of each top artist's history; rules at the top of the file)
- next_build.py: what comes next (song-to-song steps and artist hops)
- power_build.py: power climbers and lane momentum (seats in the top 500 and median move per lane since launch) (climb as a rank ratio x sqrt of plays added since launch)
- drives_build.py: the Bloomfield to Morrisville drives (Capy's rule: evening or night, mostly weekdays, 70+ minutes, nothing starting before 2:30pm)
- strays_build.py: the rule for the strays shelf (outside the lanes, at least half the artist's plays, 3+ visits 60+ days apart)
- solar_positions.json: last galaxy layout, so the map stays stable between refreshes
- page/: the dashboard's HTML and JS

Fresh-chat refresh: start a new chat and say "Pull the Almanac folder from troycapybara2/scrobblemaxxing and follow its README to refresh https://claude.ai/artifact/VooHx7b7siDnZjmLSDKAYB." No zip needed.
