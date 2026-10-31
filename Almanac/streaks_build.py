# Song of the month wall + streaks.
# song_months: the most-played song of every calendar month (ties go to the one reached first), with its album
# (deluxe and other editions folded into the base album, matching the cover art).
# streaks: the longest runs of consecutive days, weeks (Mon-Sun) and calendar months with at least one play, for
# artists, songs and albums. Top 12 for each of the nine combinations, one row per entity's longest run.
import pandas as pd, numpy as np
from albumnorm import base
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
df = pd.read_pickle('df_raw.pkl').sort_values('uts')
df['m'] = df.ts.dt.strftime('%Y-%m'); df['alb'] = df.album.map(base)
df['day'] = (df.ts.dt.tz_localize(None).dt.normalize() - pd.Timestamp('2011-01-03')).dt.days   # 2011-01-03 is a Monday
df['week'] = df.day // 7; df['mon'] = df.ts.dt.year * 12 + df.ts.dt.month - 1
rows = []
for m, g in df.groupby('m'):
    c = g.groupby(['artist', 'track']).size().sort_values(ascending=False, kind='stable')
    (a, t), n = c.index[0], int(c.iloc[0])
    alb = g[(g.artist == a) & (g.track == t)].alb.value_counts().index[0]
    rows.append(dict(month=m, track=t, artist=a, album=alb, plays=n, month_plays=len(g), runner_up=f'{c.index[1][1]} ({c.index[1][0]})' if len(c) > 1 else '', family=fam.get(la.get(a, ''), 'Other')))
pd.DataFrame(rows).to_csv('out/song_months.csv', index=False)
D0 = pd.Timestamp('2011-01-03')
def label(grain, i):
    if grain == 'day': return str((D0 + pd.Timedelta(days=int(i))).date())
    if grain == 'week': return str((D0 + pd.Timedelta(days=int(i) * 7)).date())
    return f'{int(i) // 12}-{int(i) % 12 + 1:02d}'
def longest(idx):
    u = np.unique(idx); 
    if len(u) == 0: return 0, None, None
    br = np.where(np.diff(u) != 1)[0]; starts = np.r_[0, br + 1]; ends = np.r_[br, len(u) - 1]
    L = ends - starts + 1; k = int(np.argmax(L)); return int(L[k]), u[starts[k]], u[ends[k]]
out = []
for kind, keys, minp in [('Artist', ['artist'], 30), ('Song', ['artist', 'track'], 10), ('Album', ['artist', 'alb'], 20)]:
    vc = df.groupby(keys).size(); ok = vc[vc >= minp].index
    sub = df.set_index(keys).loc[ok].reset_index() if len(keys) > 1 else df[df.artist.isin(ok)]
    for grain in ['day', 'week', 'mon']:
        res = []
        for key, g in sub.groupby(keys):
            n, s0, s1 = longest(g[grain].values)
            if n >= 2: res.append((n, key, s0, s1, g))
        res.sort(key=lambda r: (-r[0], r[2]))
        for n, key, s0, s1, g in res[:12]:
            key = key if isinstance(key, tuple) else (key,)
            plays = int(((g[grain] >= s0) & (g[grain] <= s1)).sum())
            gr = 'month' if grain == 'mon' else grain
            out.append(dict(kind=kind, grain=gr, name=key[-1], artist=key[0], length=n, start=label(gr, s0), end=label(gr, s1), plays=plays))
S = pd.DataFrame(out); S.to_csv('out/streaks.csv', index=False)
for (k, gr), g in S.groupby(['kind', 'grain'], sort=False): print(k, gr, ' | '.join(f"{r['name']} {r['length']}" for _, r in g.head(4).iterrows()))

# ---------- still going: streaks alive as of the latest scrobble (for the Lately tab) ----------
# A streak is alive if its last day/week/month is the latest one or the one before (you may just not have played yet
# today or this week). Minimums: 3 days, 3 weeks, 4 months. best = this entity's longest run at that grain ever.
last = {'day': df.day.max(), 'week': df.week.max(), 'mon': df.mon.max()}
MIN = {'day': 3, 'week': 3, 'mon': 4}
alive = []
for kind, keys, minp in [('Artist', ['artist'], 10), ('Song', ['artist', 'track'], 5), ('Album', ['artist', 'alb'], 10)]:
    recent = df[df.mon >= last['mon'] - 60]
    vc = recent.groupby(keys).size(); ok = vc[vc >= minp].index
    sub = df.set_index(keys).loc[ok].reset_index() if len(keys) > 1 else df[df.artist.isin(ok)]
    for key, g in sub.groupby(keys):
        key = key if isinstance(key, tuple) else (key,)
        for grain in ['day', 'week', 'mon']:
            u = np.unique(g[grain].values)
            if u[-1] < last[grain] - 1: continue
            n = 1
            while n < len(u) and u[-1 - n] == u[-1] - n: n += 1
            if n < MIN[grain]: continue
            best, _, _ = longest(u)
            gr = 'month' if grain == 'mon' else grain
            alive.append(dict(kind=kind, grain=gr, name=key[-1], artist=key[0], length=n, start=label(gr, u[-1] - n + 1), best=best,
                              record='yes' if n >= best else 'no', plays=int((g[grain] >= u[-1] - n + 1).sum())))
A = pd.DataFrame(alive, columns=['kind', 'grain', 'name', 'artist', 'length', 'start', 'best', 'record', 'plays'])
A = A.sort_values(['grain', 'length'], ascending=[True, False]).groupby(['kind', 'grain']).head(6)
A.to_csv('out/streaks_alive.csv', index=False)
# ---------- this month's song race ----------
cm = df.m.max(); g = df[df.m == cm]
c = g.groupby(['artist', 'track']).agg(plays=('uts', 'size'), last=('uts', 'max')).reset_index().sort_values(['plays', 'last'], ascending=[False, True]).head(8)
c['album'] = [g[(g.artist == a) & (g.track == t)].alb.value_counts().index[0] for a, t in zip(c.artist, c.track)]
c['month'] = cm; c['family'] = c.artist.map(lambda a: fam.get(la.get(a, ''), 'Other'))
c[['month', 'track', 'artist', 'album', 'plays', 'family']].to_csv('out/month_race.csv', index=False)
print(A.to_string(index=False)); print(c[['track', 'artist', 'plays']].to_string(index=False))
