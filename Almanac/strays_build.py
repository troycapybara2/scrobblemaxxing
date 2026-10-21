# Strays: songs from outside your lanes with one-hit-wonder energy that you keep coming back to.
# A song qualifies when its artist has no lane (or sits in Grab bag), the song is at least half of that artist's plays,
# and you've come back to it in 3+ separate visits (a visit starts after a gap of 60+ days).
# Title variants of the same song are merged ("Believe It or Not (Theme From...)" = "Theme From ... (Believe It or Not)").
# The page shows 5 at random (same 5 until the next refresh, plus a shuffle), skipping anything played in the last 30 days.
# my_strays.json (Capy's "Keep it coming" / "Not a stray" votes, pulled from the artifact) drops or boosts songs.
import pandas as pd, numpy as np, re, json, os
df = pd.read_pickle('df_raw.pkl').sort_values('uts')
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
DROP = {'feat', 'ft', 'remaster', 'remastered', 'version', 'single', 'edit', 'radio', 'mono', 'stereo', 'the', 'a'}
key = lambda t: ' '.join(sorted(set(w for w in re.findall(r'[a-z0-9]+', str(t).lower()) if w not in DROP)))
df['k'] = df.track.map(key)
votes = {}
if os.path.exists('my_strays.json'):
    for v in json.load(open('my_strays.json')).get('items', []): votes[(v.get('artist'), key(v.get('track')))] = v.get('vote')
NOW = df.ts.max(); art = df.artist.value_counts(); rows = []
for (a, k), g in df.groupby(['artist', 'k']):
    if len(g) < 3: continue
    l = la.get(a)
    if l is not None and l != 'Grab bag': continue
    if len(g) / art[a] < 0.5: continue
    gaps = np.diff(g.ts.values) >= np.timedelta64(60, 'D'); visits = 1 + int(gaps.sum())
    if visits < 3: continue
    vote = votes.get((a, k), '')
    if vote == 'not': continue
    m = g.ts.dt.strftime('%Y-%m').value_counts().sort_index()
    rows.append(dict(artist=a, track=g.track.value_counts().index[0], plays=len(g), visits=visits, first_play=str(g.ts.min().date()), last_play=str(g.ts.max().date()),
                     recent='yes' if g.ts.max() >= NOW.normalize() - pd.Timedelta(days=29) else 'no', keep='yes' if vote == 'keep' else 'no',
                     lane=l if isinstance(l, str) else 'No lane', months='|'.join(f'{i}:{n}' for i, n in m.items())))
S = pd.DataFrame(rows).sort_values(['visits', 'plays'], ascending=False)
S.to_csv('out/strays.csv', index=False)
print('strays', len(S), 'eligible now', int((S.recent == 'no').sum()))
