# First listens: the day you first played each of your top 100 artists, the song that started it, and how much you
# played them after. Feeds the first listens timeline (a beeswarm along 2011 to now).
import pandas as pd
df = pd.read_pickle('df_raw.pkl').sort_values('uts')
top = df.artist.value_counts().head(100)
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
f = df[df.artist.isin(top.index)].groupby('artist').first()
F = pd.DataFrame({'artist': f.index, 'first_play': f.ts.dt.strftime('%Y-%m-%d').values, 'first_track': f.track.values,
                  'plays': top.reindex(f.index).values, 'rank': top.rank(ascending=False, method='first').reindex(f.index).astype(int).values})
F['lane'] = F.artist.map(la).fillna('No lane'); F['family'] = F.lane.map(fam).fillna('Other')
F.sort_values('first_play').to_csv('out/first_listens.csv', index=False)
print(F.sort_values('first_play').groupby(F.first_play.str[:4]).size().to_dict())
