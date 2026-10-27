# Long gone: artists you played 50+ times with no play in the last 18 months.
# The page shows 5 at random (same 5 until the next refresh, plus a shuffle), with Bring it back / Gone for good votes.
# my_gone.json (those votes, pulled from the artifact) drops "Gone for good" artists and boosts "Bring it back".
import pandas as pd, json, os
df = pd.read_pickle('df_raw.pkl').sort_values('uts')
NOW = df.ts.max(); cut = NOW.normalize() - pd.Timedelta(days=548)
votes = {}
if os.path.exists('my_gone.json'):
    for v in json.load(open('my_gone.json')).get('items', []): votes[v.get('artist')] = v.get('vote')
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
g = df.groupby('artist').agg(plays=('uts', 'size'), last=('ts', 'max'), first=('ts', 'min'))
g = g[(g.plays >= 50) & (g['last'] < cut)]
rows = []
for a, r in g.iterrows():
    if votes.get(a) == 'not': continue
    x = df[df.artist == a]; y = x.ts.dt.year.value_counts().sort_index()
    tt = x.track.value_counts()
    rows.append(dict(artist=a, plays=int(r.plays), first_play=str(r['first'].date()), last_play=str(r['last'].date()),
                     years_gone=round((NOW - r['last']).days / 365.25, 1), peak_year=int(y.idxmax()), peak_plays=int(y.max()),
                     top_track=tt.index[0], top_track_plays=int(tt.iloc[0]), last_track=x.track.iloc[-1],
                     lane=la.get(a, 'No lane'), keep='yes' if votes.get(a) == 'keep' else 'no', years='|'.join(f'{i}:{n}' for i, n in y.items())))
G = pd.DataFrame(rows).sort_values('plays', ascending=False)
G.to_csv('out/long_gone.csv', index=False)
print('long gone', len(G)); print(G.head(12)[['artist', 'plays', 'peak_year', 'last_play', 'top_track']].to_string(index=False))
