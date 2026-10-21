# "Lately" tab: the last 7 days, a 13-week bump chart, the last 30 days vs the year before, and new artists from the last 90 days.
# Every window ends at the latest scrobble (not the clock), so a rebuild of the same data gives the same answer.
import pandas as pd, numpy as np, collections
exec(open('buckets6.py').read())          # gives df (all scrobbles), E (2023+ with bucket) and assign (artist -> lane)
FAM = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)  # lane -> family (run after now_life_build.py)
O = 'out/'
d = df.sort_values('uts').copy()
NOW = d.ts.max(); DAY = pd.Timedelta(days=1)
TODAY = NOW.normalize() + DAY                     # windows are whole days ending with the latest scrobble's day
start = lambda n: TODAY - n * DAY
lane = lambda a: assign.get(a, 'Not tagged yet')

# ---------- last 7 days ----------
w0 = start(7); p0 = start(14)
wk = d[d.ts >= w0]; prev = d[(d.ts >= p0) & (d.ts < w0)]
first = d.groupby('artist').ts.min()
newA = first[first >= w0]
ev = []
for a in newA.index:
    ev.append(dict(kind='First listen', date=str(newA[a].date()), artist=a, track='', detail=(lambda k: f"{k} play" + ('' if k == 1 else 's') + ' so far')(int((wk.artist == a).sum())), n=int((wk.artist == a).sum())))
def crossings(key, steps, kind):
    before = d[d.ts < w0].groupby(key).size(); now = d.groupby(key).size()
    for k, n in now.items():
        b = int(before.get(k, 0))
        hit = [s for s in steps if b < s <= n]
        if not hit: continue
        s = max(hit); grp = d[(d[key[0]] == k[0]) & (d[key[1]] == k[1])] if isinstance(key, list) else d[d[key] == k]
        when = grp.ts.iloc[s - 1]
        a, t = (k if isinstance(key, list) else (k, ''))
        ev.append(dict(kind=kind, date=str(when.date()), artist=a, track=t, detail=f"{s:,}th play", n=s))
crossings('artist', [100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000], 'Artist milestone')
crossings(['artist', 'track'], [25, 50, 75, 100, 150, 200, 250, 300], 'Song milestone')
rb = d[d.ts < w0].artist.value_counts().rank(method='first', ascending=False)
rn = d.artist.value_counts().rank(method='first', ascending=False)
mv = pd.DataFrame({'before': rb, 'now': rn}).dropna()
mv = mv[(mv.now <= 250) & (mv.before - mv.now >= 2)]
mv['up'] = mv.before - mv.now
for a, r in mv.sort_values(['up', 'now'], ascending=[False, True]).head(6).iterrows():
    ev.append(dict(kind='Climbed all-time', date=str(NOW.date()), artist=a, track='', detail=f"#{int(r.before)} to #{int(r.now)}", n=int(r.up)))
E7 = pd.DataFrame(ev, columns=['kind', 'date', 'artist', 'track', 'detail', 'n'])
korder = {'First listen': 0, 'Artist milestone': 1, 'Song milestone': 2, 'Climbed all-time': 3}
E7 = E7.sort_values(['kind', 'n'], key=lambda s: s.map(korder) if s.name == 'kind' else -s, ascending=[True, True])
E7 = pd.concat([g.head(8) for _, g in E7.groupby('kind', sort=False)]).drop(columns='n')
E7['lane'] = E7.artist.map(lane); E7['family'] = E7.lane.map(FAM).fillna('Other')
E7.to_csv(O + 'recent_events.csv', index=False)

# ---------- 13-week bump chart: each weekly point ranks artists by their trailing 28 days, which smooths out one-off binges ----------
rows = []
for i in range(12, -1, -1):
    end = TODAY - i * 7 * DAY; g = d[(d.ts >= end - 28 * DAY) & (d.ts < end)]
    vc = g.artist.value_counts()
    vc = vc.sort_index().sort_values(ascending=False, kind='stable')
    for r, (a, n) in enumerate(vc.items(), 1):
        rows.append(dict(week=str((end - DAY).date()), artist=a, rank=r, plays=int(n)))
B = pd.DataFrame(rows)
keep = set(B[B['rank'] <= 10].artist)
B = B[B.artist.isin(keep)].copy(); B['lane'] = B.artist.map(lane); B['family'] = B.lane.map(FAM).fillna('Other')
B.to_csv(O + 'bump_90d.csv', index=False)

# ---------- last 30 days vs the 12 months before ----------
T = E[E.bucket != 'Everything else']             # shares are of tagged plays, like the 2026 lane ranks
m30 = T[T.ts >= start(30)]; yr = T[(T.ts < start(30)) & (T.ts >= start(395))]
s30 = m30.bucket.value_counts(normalize=True); syr = yr.bucket.value_counts(normalize=True)
LM = pd.DataFrame({'share_30d': s30, 'share_normal': syr}).fillna(0)
LM['plays_30d'] = m30.bucket.value_counts().reindex(LM.index).fillna(0).astype(int)
LM['change_pts'] = ((LM.share_30d - LM.share_normal) * 100).round(1)
LM = LM.round(4).rename_axis('lane').reset_index(); LM['family'] = LM.lane.map(FAM).fillna('Other')
LM = LM.sort_values('share_30d', ascending=False)
LM.to_csv(O + 'lane_month.csv', index=False)
tagged = LM
up = tagged.sort_values('change_pts', ascending=False).iloc[0]; down = tagged.sort_values('change_pts').iloc[0]
# the last time a 30-day window had this lane this high (checked every 7 days back to 2023)
since = ''
t = start(30)                                   # only 30-day windows that ended before this one began
while t > T.ts.min() + 30 * DAY:
    g = T[(T.ts >= t - 30 * DAY) & (T.ts < t)]
    if len(g) and (g.bucket == up.lane).mean() >= up.share_30d: since = t.strftime('%Y-%m'); break
    t -= 7 * DAY

# ---------- new artists from the last 90 days ----------
n90 = first[first >= start(90)].index
nd = d[d.artist.isin(n90)].copy(); nd['day'] = nd.ts.dt.date
NA = nd.groupby('artist').agg(first_play=('ts', 'min'), last_play=('ts', 'max'), plays=('uts', 'size'), days=('day', 'nunique')).reset_index()
NA['status'] = np.where(NA.days >= 3, 'Stuck', np.where(NA.days == 2, 'Came back once', 'One-day try'))
NA['first_play'] = NA.first_play.dt.date.astype(str); NA['last_play'] = NA.last_play.dt.date.astype(str)
NA['lane'] = NA.artist.map(lane); NA['family'] = NA.lane.map(FAM).fillna('Other')
NA = NA.sort_values(['days', 'plays'], ascending=False)
NA.to_csv(O + 'recent_new_artists.csv', index=False)

# ---------- headline numbers ----------
tt = wk.groupby(['artist', 'track']).size().sort_values(ascending=False)
ta = wk.artist.value_counts()
K = [('window_start', str(w0.date()), 'First day of the last 7 days'), ('window_end', str(NOW.date()), 'Latest scrobble'),
     ('plays_7d', len(wk), 'Plays in the last 7 days'), ('plays_prev_7d', len(prev), 'Plays in the 7 days before'),
     ('artists_7d', wk.artist.nunique(), 'Artists played in the last 7 days'), ('new_artists_7d', len(newA), 'First-time artists in the last 7 days'),
     ('top_artist_7d', ta.index[0] if len(ta) else '', 'Most-played artist, last 7 days'), ('top_artist_7d_plays', int(ta.iloc[0]) if len(ta) else 0, 'Their plays'),
     ('top_track_7d', tt.index[0][1] if len(tt) else '', 'Most-played song, last 7 days'), ('top_track_7d_artist', tt.index[0][0] if len(tt) else '', 'By'),
     ('top_track_7d_plays', int(tt.iloc[0]) if len(tt) else 0, 'Its plays'),
     ('plays_30d', int((d.ts >= start(30)).sum()), 'Plays in the last 30 days'), ('lane_up', up.lane, 'Lane up most vs the year before'), ('lane_up_share', up.share_30d, 'Its share of the last 30 days'),
     ('lane_up_normal', up.share_normal, 'Its share over the 12 months before'), ('lane_up_since', since, 'Last month it was this high (blank: not since 2023)'),
     ('lane_down', down.lane, 'Lane down most'), ('lane_down_share', down.share_30d, 'Its share of the last 30 days'), ('lane_down_normal', down.share_normal, 'Its share over the 12 months before'),
     ('new_90d', len(NA), 'First-time artists in the last 90 days'), ('new_90d_stuck', int((NA.status == 'Stuck').sum()), 'Played on 3+ separate days'),
     ('new_90d_once', int((NA.status == 'One-day try').sum()), 'Only played on one day')]
pd.DataFrame(K, columns=['metric', 'value', 'label']).to_csv(O + 'recent_week.csv', index=False)
print(pd.DataFrame(K, columns=['metric', 'value', 'label'])[['metric', 'value']].to_string(index=False))
print(E7.to_string(index=False)); print(B[B.week == B.week.max()].head(10).to_string(index=False)); print(LM.head(8).to_string(index=False)); print(NA.head(12).to_string(index=False))
