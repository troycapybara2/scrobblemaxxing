# Big months and steady stretches.
# Big months: artists whose best calendar month reached 100+ plays (the 300+ club is the top tier), with every
# 100+ month they had. Steady: best month 50 to 99 plays, and 10+ plays a month on average across their best
# 12-month stretch (calendar months, empty months count as zero). Slow and steady: never a 50-play month, ranked by
# that same best 12-month average, so they were always around without ever binging.
import pandas as pd, numpy as np
df = pd.read_pickle('df_raw.pkl'); df['m'] = df.ts.dt.strftime('%Y-%m')
M = df.groupby(['artist', 'm']).size().rename('n').reset_index()
allm = pd.period_range(df.ts.min().strftime('%Y-%m'), df.ts.max().strftime('%Y-%m'), freq='M').strftime('%Y-%m')
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
F = lambda a: fam.get(la.get(a, ''), 'Other')
big, steady, slow = [], [], []
for a, g in M.groupby('artist'):
    s = g.set_index('m').n.reindex(allm, fill_value=0)
    pk = int(s.max())
    if pk >= 100:
        hot = s[s >= 100]
        big.append(dict(artist=a, peak_month=s.idxmax(), peak_plays=pk, tier='300+' if pk >= 300 else '100+', months_100=int((s >= 100).sum()),
                        months_300=int((s >= 300).sum()), plays=int(s.sum()), family=F(a), hot_months='|'.join(f'{m}:{int(n)}' for m, n in hot.items())))
    elif s.sum() >= 60:
        r = s.rolling(12).sum(); end = r.idxmax(); best = r.max() / 12
        if best >= (10 if pk >= 50 else 5):
            i = list(allm).index(end)
            (steady if pk >= 50 else slow).append(dict(artist=a, avg_per_month=round(best, 1), start=allm[i - 11], end=end, peak_month=s.idxmax(), peak_plays=pk,
                               plays=int(s.sum()), family=F(a), months=' '.join(str(int(x)) for x in s.iloc[i - 11:i + 1])))
B = pd.DataFrame(big).sort_values(['peak_plays'], ascending=False); B.insert(0, 'rank', range(1, len(B) + 1))
S = pd.DataFrame(steady).sort_values('avg_per_month', ascending=False); S.insert(0, 'rank', range(1, len(S) + 1))
W = pd.DataFrame(slow).sort_values('avg_per_month', ascending=False); W.insert(0, 'rank', range(1, len(W) + 1))
B.to_csv('out/big_months.csv', index=False); S.to_csv('out/steady_stretches.csv', index=False); W.to_csv('out/slow_steady.csv', index=False)
print(len(B), (B.tier == '300+').sum(), len(S), len(W)); print(W.head(12)[['artist', 'avg_per_month', 'start', 'end', 'peak_plays']].to_string(index=False)); print(B.head(12)[['artist', 'peak_month', 'peak_plays', 'months_100']].to_string(index=False)); print(S.head(12)[['artist', 'avg_per_month', 'start', 'end', 'peak_plays']].to_string(index=False))
