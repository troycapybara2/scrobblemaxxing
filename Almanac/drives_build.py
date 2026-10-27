# The Bloomfield to Morrisville drives (Sep 2020 to Sep 2021): ~90 minutes each way to Katie's.
# Capy's rule: usually evening or night, mostly weekdays, 70+ minutes, and anything starting before 2:30pm is unlikely.
# A drive = an unbroken session (no gap over 10 minutes) that starts at 2:30pm or later and runs 70 to 150 minutes.
# Songs are ranked by how much more often they played on drives than in the rest of that year's listening.
import pandas as pd, numpy as np
df = pd.read_pickle('df_raw.pkl').sort_values('uts').reset_index(drop=True)
b = df[(df.ts >= '2020-09-01') & (df.ts < '2021-09-15')].copy()
b['sess'] = (b.uts.diff().fillna(1e9) > 10 * 60).cumsum()
S = b.groupby('sess').agg(start=('ts', 'min'), end=('ts', 'max'), plays=('uts', 'size'))
S['minutes'] = ((S.end - S.start).dt.total_seconds() / 60).round().astype(int)
h = S.start.dt.hour + S.start.dt.minute / 60
D = S[(h >= 14.5) & (S.minutes >= 70) & (S.minutes <= 150)].copy()
on = b[b.sess.isin(D.index)]; off = b[~b.sess.isin(D.index)]
D['top_artist'] = on.groupby('sess').artist.agg(lambda s: s.value_counts().index[0])
IDS = set(D.index); D = D.reset_index(drop=True)
out = pd.DataFrame({'date': D.start.dt.date.astype(str), 'day': D.start.dt.day_name(), 'start': D.start.dt.strftime('%-I:%M %p'),
                    'minutes': D.minutes, 'plays': D.plays, 'top_artist': D.top_artist})
out.to_csv('out/drives.csv', index=False)
c_on = on.groupby(['artist', 'track']).size(); c_off = off.groupby(['artist', 'track']).size()
T = pd.DataFrame({'plays': c_on}).join(c_off.rename('elsewhere')).fillna(0)
T['times_more_likely'] = ((T.plays / len(on)) / ((T.elsewhere + 1) / len(off))).round(1)
T = T[T.plays >= 3].sort_values(['times_more_likely', 'plays'], ascending=False).head(25).reset_index()
T.insert(0, 'rank', range(1, len(T) + 1)); T['plays'] = T.plays.astype(int); T['elsewhere'] = T.elsewhere.astype(int)
T[['rank', 'track', 'artist', 'plays', 'elsewhere', 'times_more_likely']].to_csv('out/drive_songs.csv', index=False)
jp = b[(b.artist == 'BabyTron') & b.track.str.contains('Jurassic', case=False)]
A = on.artist.value_counts().head(10)
K = [('drives', len(D), 'Likely drives found'), ('drive_minutes', int(D.minutes.sum()), 'Minutes of music on them'), ('drive_plays', len(on), 'Scrobbles on them'),
     ('median_minutes', int(D.minutes.median()), 'Typical drive length'), ('weekday_drives', int((D.start.dt.dayofweek < 5).sum()), 'Drives on a weekday'), ('top_drive_artist', A.index[0], 'Most-played artist on the drives'),
     ('top_drive_artist_plays', int(A.iloc[0]), 'Their plays on the drives'), ('jurassic_park_year', len(jp), 'Jurassic Park plays that year'),
     ('jurassic_park_drives', int(jp.sess.isin(IDS).sum()), 'Jurassic Park plays on the drives'),
     ('jurassic_park_peak', jp.ts.dt.strftime('%Y-%m').value_counts().index[0] if len(jp) else '', 'Month Jurassic Park peaked')]
pd.DataFrame(K, columns=['metric', 'value', 'label']).to_csv('out/drive_stats.csv', index=False)
print(pd.DataFrame(K)[[0, 1]].to_string(index=False)); print(T.head(15).to_string(index=False)); print(out.day.value_counts().to_dict())
