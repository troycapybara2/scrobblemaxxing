# Map over time + local while you lived there. Run after places_build.py and life_build.py.
# place_year: for every place and year, plays through the end of that year from its artists (cumulative) and how many
# of its artists you had heard by then, so the map can fill in year by year.
# local_*: for each place you lived (a life chapter), how much of that chapter's listening came from artists whose
# hometown is within 75 miles of where you were living.
import pandas as pd, numpy as np
exec(open('life.py').read().split('def chap')[0])          # CH: (chapter, start, end, note)
HOME = {'Milltown, NJ': (40.456, -74.443), 'Poughkeepsie, NY': (41.70, -73.92), 'Milltown, NJ (again)': (40.456, -74.443),
        'Bloomfield, NJ': (40.807, -74.188), 'Philly': (39.95, -75.17), 'Bristol': (40.10, -74.85)}
R = 75   # miles
df = pd.read_pickle('df_raw.pkl')
P = pd.read_csv('out/artist_places.csv', keep_default_na=False)
d = df[df.artist.isin(P.artist)].copy(); d['y'] = d.ts.dt.year
lab = dict(zip(P.artist, P.label))
d['label'] = d.artist.map(lab)
Y = range(int(df.ts.dt.year.min()), int(df.ts.dt.year.max()) + 1)
first = d.groupby('artist').ts.min().dt.year
rows = []
for lb, g in d.groupby('label'):
    py = g.groupby('y').size().reindex(Y, fill_value=0).cumsum()
    arts = g.artist.unique()
    for y in Y:
        if py[y] == 0: continue
        rows.append(dict(label=lb, year=y, plays=int(py[y]), artists=int(sum(first[a] <= y for a in arts)), new_artists=int(sum(first[a] == y for a in arts))))
pd.DataFrame(rows).to_csv('out/place_year.csv', index=False)
miles = lambda la1, lo1, la2, lo2: 3958.8 * 2 * np.arcsin(np.sqrt(np.sin(np.radians(la2 - la1) / 2) ** 2 + np.cos(np.radians(la1)) * np.cos(np.radians(la2)) * np.sin(np.radians(lo2 - lo1) / 2) ** 2))
T = lambda s: pd.Timestamp(s, tz='America/New_York')
lat = dict(zip(P.artist, P.lat)); lon = dict(zip(P.artist, P.lon))
crow, prow = [], []
for ch, a, b, _ in CH:
    if ch not in HOME: continue
    hl, ho = HOME[ch]; w = df[(df.ts >= T(a)) & (df.ts < T(b))]; wp = w[w.artist.isin(P.artist)]
    dist = wp.artist.map(lambda x: miles(hl, ho, float(lat[x]), float(lon[x])))
    loc = wp[dist <= R]
    top = loc.artist.value_counts().head(6)
    crow.append(dict(chapter=ch, start=a, home_lat=hl, home_lon=ho, plays=len(w), plays_placed=len(wp), plays_local=len(loc),
                     local_share=round(len(loc) / max(1, len(wp)), 3), top_local=' | '.join(f'{x}:{n}' for x, n in top.items())))
    for lb, g in wp.groupby(wp.artist.map(lab)):
        x0 = g.artist.iloc[0]
        prow.append(dict(chapter=ch, label=lb, lat=lat[x0], lon=lon[x0], plays=len(g), local='yes' if miles(hl, ho, float(lat[x0]), float(lon[x0])) <= R else 'no'))
pd.DataFrame(crow).to_csv('out/local_chapters.csv', index=False)
pd.DataFrame(prow).to_csv('out/local_places.csv', index=False)
print(pd.DataFrame(crow)[['chapter', 'plays_placed', 'plays_local', 'local_share', 'top_local']].to_string(index=False))
