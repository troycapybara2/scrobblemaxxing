# What comes next: songs you play right after other songs. Two plays are a step when they're back to back within
# 15 minutes and are different songs. Steps between two songs from the same album are left out (that's just the album
# playing), so what's left are sequences you made.
import pandas as pd, collections
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
FAM = lambda a: fam.get(la.get(a, ''), 'Other')
df = pd.read_pickle('df_raw.pkl').sort_values('uts').reset_index(drop=True)
gap = df.uts.diff().fillna(1e9)
key = list(zip(df.artist, df.track)); alb = df.album.str.lower().str.strip().tolist()
pair = collections.Counter(); first = {}; last = {}
for i in range(1, len(df)):
    if gap[i] > 900 or key[i] == key[i - 1]: continue
    if alb[i] and alb[i] == alb[i - 1]: continue
    p = (key[i - 1], key[i]); pair[p] += 1; first.setdefault(p, df.ts[i]); last[p] = df.ts[i]
fromN = collections.Counter(); 
for (a, b), n in pair.items(): fromN[a] += n
rows = [dict(from_track=a[1], from_artist=a[0], to_track=b[1], to_artist=b[0], times=n, share=round(n / fromN[a], 3),
             first=str(first[(a, b)].date()), last=str(last[(a, b)].date()), from_family=FAM(a[0]), to_family=FAM(b[0])) for (a, b), n in pair.most_common(40)]
pd.DataFrame(rows).to_csv('out/next_pairs.csv', index=False)
# artist to artist: where you go next after your top artists (different artist only)
ap = collections.Counter()
for (a, b), n in pair.items():
    if a[0] != b[0]: ap[(a[0], b[0])] += n
topA = df.artist.value_counts().head(100).index
arow = []
for A in topA:
    outs = sorted(((n, b) for (a, b), n in ap.items() if a == A), reverse=True)
    tot = sum(n for n, _ in outs)
    for n, b in outs[:5]: arow.append(dict(artist=A, next_artist=b, times=n, share=round(n / tot, 3), family=FAM(A), next_family=FAM(b)))
pd.DataFrame(arow).to_csv('out/next_artists.csv', index=False)
print(pd.DataFrame(rows).head(12)[['from_track', 'from_artist', 'to_track', 'to_artist', 'times', 'share']].to_string(index=False))

