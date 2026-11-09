# Albums to own: which albums you actually listen to as albums, for the MusicBee library.
# Capy's rule: plays alone don't make an album essential. 40 plays of one song isn't it; 36 plays spread
# across 12 songs (the whole thing, three times) is. So the score is "times through", not plays:
#   T     = the album's size, estimated as the songs you've played from it (at least 6, since Last.fm has no tracklists)
#   need  = 60% of T (at most 10 songs): how many songs count as "most of the album"
#   times_through = the play count that `need` different songs have all reached
#   full_sittings = sessions (30-minute gaps) where you played `need`+ different songs from it
# Plays of a song's single release are credited to the album the song lives on.
import pandas as pd, numpy as np, re, math, json, os
df = pd.read_pickle('df.pkl')
df = df[df.uts > 1e9].copy()
df['sess'] = (df.uts.diff().fillna(1e9) > 1800).cumsum()
def tnorm(t):
    t = str(t).lower()
    t = re.sub(r'\s*[\(\[](feat|ft|with|prod)[^\)\]]*[\)\]]', '', t)
    t = re.sub(r'\s+-\s+.*(remaster|version|edit|mix|mono|stereo|live|acoustic).*$', '', t)
    t = re.sub(r'\s*[\(\[][^\)\]]*(remaster|version|edit|explicit|clean)[^\)\]]*[\)\]]', '', t)
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()
df['tk'] = df.track.map(tnorm)
al = df.album.str.lower().str.strip()
df['single'] = (df.album == '') | al.str.endswith(' - single') | al.str.endswith(' - ep') & False | (al == df.track.str.lower().str.strip()) | (al.map(tnorm) == df.tk)
# home album for each song: the non-single album with the most plays of it
home = (df[~df.single].groupby(['artist', 'tk', 'album']).size().reset_index(name='n')
        .sort_values('n', ascending=False).drop_duplicates(['artist', 'tk']).set_index(['artist', 'tk']).album)
key = list(zip(df.artist, df.tk))
df['home'] = [home.get(k, a) if s else a for k, a, s in zip(key, df.album, df.single)]
df['credited'] = df.single & (df.home != df.album)
A = df[(df.home != '') & ~(df.single & ~df.credited)].copy()   # leave out singles with no album to go to
A['y'] = A.ts.dt.year
rows = []
for (artist, album), g in A.groupby(['artist', 'home'], sort=False):
    if len(g) < 15: continue
    tc = g.groupby('tk').agg(n=('uts', 'size'), name=('track', lambda s: s.value_counts().index[0])).sort_values('n', ascending=False)
    songs = len(tc); T = max(songs, 6); need = min(10, math.ceil(0.6 * T))
    times = int(tc.n.iloc[need - 1]) if songs >= need else 0
    per = g.groupby('sess').tk.nunique()
    sittings = int((per >= need).sum()) if songs >= need else 0
    yrs = g.groupby('y').size()
    rows.append(dict(artist=artist, album=album, plays=len(g), songs=songs, need=need, times_through=times,
        full_sittings=sittings, songs_5plus=int((tc.n >= 5).sum()), top_track=tc.name.iloc[0], top_track_plays=int(tc.n.iloc[0]),
        top_track_share=round(tc.n.iloc[0] / len(g), 3), years_played=int((yrs >= 5).sum()),
        first=g.ts.min().strftime('%Y-%m-%d'), last=g.ts.max().strftime('%Y-%m-%d'),
        single_plays_credited=int(g.credited.sum()), peak_year=int(yrs.idxmax())))
R = pd.DataFrame(rows)
def tier(r):
    if r.times_through >= 8 or (r.times_through >= 5 and r.full_sittings >= 5): return 'Essential'
    if r.times_through >= 3 or (r.times_through >= 2 and r.full_sittings >= 2): return 'Should own'
    if r.times_through >= 2 or (r.times_through >= 1 and r.songs_5plus >= 4): return 'On the bubble'
    if r.top_track_plays >= 25: return 'Just the songs'
    return ''
R['tier'] = R.apply(tier, axis=1)
R = R[R.tier != ''].copy()
R['kind'] = 'album'
# standalone singles with no album to credit them to: 25+ plays goes on the songs list
S = df[df.single & ~df.credited]
S = (S.groupby(['artist', 'tk']).agg(plays=('uts', 'size'), track=('track', lambda s: s.value_counts().index[0]),
     album=('album', lambda s: s.value_counts().index[0]), first=('ts', 'min'), last=('ts', 'max'),
     years_played=('ts', lambda s: int((s.dt.year.value_counts() >= 5).sum())), peak_year=('ts', lambda s: int(s.dt.year.value_counts().idxmax())))
     .reset_index())
S = S[S.plays >= 25].copy()
S['album'] = [a if a else t for a, t in zip(S.album, S.track)]
S = S.drop_duplicates(['artist', 'album'])
S = S.assign(tier='Just the songs', kind='single', songs=1, need=0, times_through=0, full_sittings=0, songs_5plus=1, top_track=S.track,
             top_track_plays=S.plays, top_track_share=1.0, single_plays_credited=0,
             first=S['first'].dt.strftime('%Y-%m-%d'), last=S['last'].dt.strftime('%Y-%m-%d'))
S = S[~S.set_index(['artist', 'album']).index.isin(R.set_index(['artist', 'album']).index)]
R = pd.concat([R, S.drop(columns=['tk', 'track'])], ignore_index=True)
order = {'Essential': 0, 'Should own': 1, 'On the bubble': 2, 'Just the songs': 3}
R['t'] = R.tier.map(order)
R['sortplays'] = np.where(R.tier == 'Just the songs', R.top_track_plays, R.plays)
R = R.sort_values(['t', 'times_through', 'full_sittings', 'sortplays'], ascending=[True, False, False, False]).drop(columns=['t', 'sortplays'])
R['rank'] = range(1, len(R) + 1)
sc = pd.read_csv('artist_lanes.csv').rename(columns={'lane': 'scene'})[['artist', 'scene']].drop_duplicates('artist')
R = R.merge(sc, on='artist', how='left'); R['scene'] = R.scene.fillna('Long tail')
# per-song plays for each album (top 15, most played first) as "song:plays | song:plays", for the song strips
tl = {}
for (artist, album), g in A.groupby(['artist', 'home'], sort=False):
    tc = g.groupby('tk').agg(n=('uts', 'size'), name=('track', lambda s: s.value_counts().index[0])).sort_values('n', ascending=False).head(15)
    tl[(artist, album)] = ' | '.join(str(nm).replace('|', '/') + ':' + str(n) for nm, n in zip(tc.name, tc.n))
R['tracks'] = [tl.get((a, b), '') if k == 'album' else str(t).replace('|', '/') + ':' + str(p) for a, b, k, t, p in zip(R.artist, R.album, R.kind, R.top_track, R.top_track_plays)]
os.makedirs('out', exist_ok=True)
cols = ['rank', 'tier', 'kind', 'artist', 'album', 'times_through', 'full_sittings', 'plays', 'songs', 'need', 'songs_5plus', 'top_track', 'top_track_plays', 'top_track_share', 'years_played', 'peak_year', 'first', 'last', 'single_plays_credited', 'scene', 'tracks']
R[cols].to_csv('out/own_albums.csv', index=False)
T = R.groupby('tier', sort=False).agg(albums=('album', 'size'), plays=('plays', 'sum'), median_times_through=('times_through', 'median')).reset_index()
T['order'] = T.tier.map(order); T = T.sort_values('order')
T[['tier', 'albums', 'plays', 'median_times_through']].to_csv('out/own_tiers.csv', index=False)
print('own', R.tier.value_counts().to_dict())
