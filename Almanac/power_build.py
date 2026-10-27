# Power climbers: climbing since the leaderboard app launched (Dec 9, 2025), weighted by the plays it took.
# Climbing is scored as a ratio, so #40 to #20 counts the same as #800 to #400 (moving up near the top is hard),
# then multiplied by the square root of plays added since launch. power = ln(rank at launch / rank now) x sqrt(plays added).
# Artists in today's top 500 who were already ranked at launch.
import pandas as pd, numpy as np
df = pd.read_pickle('df_raw.pkl')
LAUNCH = pd.Timestamp('2025-12-09 21:16', tz='America/New_York')
a = df[df.ts <= LAUNCH].artist.value_counts(); b = df.artist.value_counts()
T = pd.DataFrame({'rank_launch': a.rank(method='first', ascending=False), 'rank_now': b.rank(method='first', ascending=False), 'plays_launch': a, 'plays_now': b})
T = T[(T.rank_now <= 500) & T.rank_launch.notna()].copy()
T['plays_added'] = (T.plays_now - T.plays_launch).astype(int)
T['places'] = (T.rank_launch - T.rank_now).astype(int)
T = T[T.places > 0]
T['power'] = (np.log(T.rank_launch / T.rank_now) * np.sqrt(T.plays_added)).round(2)
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
T = T.sort_values('power', ascending=False).head(15).rename_axis('artist').reset_index()
T.insert(0, 'power_rank', range(1, len(T) + 1))
T['lane'] = T.artist.map(la).fillna('No lane'); T['family'] = T.lane.map(fam).fillna('Other')
T = T.astype({'rank_launch': int, 'rank_now': int, 'plays_launch': int, 'plays_now': int})
T[['power_rank', 'artist', 'power', 'rank_launch', 'rank_now', 'places', 'plays_added', 'plays_now', 'lane', 'family']].to_csv('out/power_climbers.csv', index=False)
print(T[['power_rank', 'artist', 'power', 'rank_launch', 'rank_now', 'plays_added', 'family']].to_string(index=False))

# ---------- lane momentum: how each lane's artists moved in the all-time ranks since launch ----------
# seats = artists in the top 500; median_move = median places gained by the lane's artists ranked in the top 1,000 both times.
ra = a.rank(method='first', ascending=False); rb = b.rank(method='first', ascending=False)
M = pd.DataFrame({'rank_launch': ra, 'rank_now': rb}); M['lane'] = M.index.map(lambda x: la.get(x, 'Long tail'))
rows = []
for ln, g in M.groupby('lane'):
    if ln == 'Long tail': continue
    both = g[(g.rank_launch <= 1000) & (g.rank_now <= 1000)]
    rows.append(dict(lane=ln, family=fam.get(ln, 'Other'), seats_now=int((g.rank_now <= 500).sum()), seats_launch=int((g.rank_launch <= 500).sum()),
                     median_move=float((both.rank_launch - both.rank_now).median()) if len(both) else 0.0, artists_compared=len(both)))
LM = pd.DataFrame(rows); LM['seat_change'] = LM.seats_now - LM.seats_launch
LM = LM[(LM.seats_now > 0) | (LM.seats_launch > 0)].sort_values(['seat_change', 'median_move'], ascending=False)
LM[['lane', 'family', 'seats_now', 'seats_launch', 'seat_change', 'median_move', 'artists_compared']].to_csv('out/lane_momentum.csv', index=False)
print(LM.to_string(index=False))
