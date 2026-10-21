#!/bin/bash
# Pulls everything the build needs from github.com/troycapybara2/scrobblemaxxing, then rebuilds df_raw.pkl.
set -e
R=https://raw.githubusercontent.com/troycapybara2/scrobblemaxxing/main
curl -sSfL -o latest.csv $R/data/scrobbles.csv
curl -sSfL -o leaderboard_history.json $R/lastfm_cache/leaderboard_history.json
cp art3.json /tmp/art3.json
python3 - <<'PY'
import pandas as pd
df=pd.read_csv('latest.csv'); df=df[df.uts>1e9].copy()
df['ts']=pd.to_datetime(df.uts,unit='s',utc=True).dt.tz_convert('America/New_York')
df['album']=df.album.fillna(''); df=df.sort_values('uts').reset_index(drop=True)
df.to_pickle('df_raw.pkl'); print(len(df),'scrobbles through',df.ts.max())
PY
