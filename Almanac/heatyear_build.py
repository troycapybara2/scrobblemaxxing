# Heating up this year: the zoomed-out version of "Heating up right now". Plays in the last 365 days against the
# average plays per year across the 5 years before that, for artists you were already playing by the end of 2021
# (so there's a real 5-year baseline). Only artists outpacing their average, with 25+ plays this year.
import pandas as pd
from albumnorm import base
df = pd.read_pickle('df_raw.pkl'); NOW = df.ts.max(); Y = pd.Timedelta(days=365)
cur = df[df.ts > NOW - Y]; prev = df[(df.ts <= NOW - Y) & (df.ts > NOW - 6 * Y)]
first = df.groupby('artist').ts.min()
old = set(first[first < pd.Timestamp('2022-01-01', tz=NOW.tz)].index)
c = cur.artist.value_counts(); p = prev.artist.value_counts() / 5
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
rows = []
for a, n in c.items():
    if a not in old or n < 25: continue
    avg = float(p.get(a, 0)); ratio = n / max(avg, 1)
    if ratio <= 1: continue
    alb = df[df.artist == a].album.map(base).value_counts().index[0]
    rows.append(dict(artist=a, plays_1y=int(n), avg_5y=round(avg, 1), ratio=round(ratio, 1), first_year=int(first[a].year), top_album=alb,
                     lane=la.get(a, 'No lane'), family=fam.get(la.get(a, ''), 'Other')))
H = pd.DataFrame(rows).sort_values('ratio', ascending=False).head(15)
H.to_csv('out/heat_year.csv', index=False)
print(H[['artist', 'plays_1y', 'avg_5y', 'ratio', 'first_year']].to_string(index=False))
