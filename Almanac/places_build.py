# Artist map: where your artists are from. artist_places.csv is the hand list (source = Claude or Capy);
# Capy's own answers in my_categorize.json (q = place) override it. Aggregates to one dot per place.
import pandas as pd, json, os
df = pd.read_pickle('df_raw.pkl'); vc = df.artist.value_counts()
P = pd.read_csv('artist_places.csv', keep_default_na=False); P['whole_state'] = False   # whole_state: only the state is known (a dot in the middle of it)
if os.path.exists('my_categorize.json'):
    for x in json.load(open('my_categorize.json'))['answers']:
        if x.get('q') == 'place':
            P = P[P.artist != x['artist']]
            P = pd.concat([P, pd.DataFrame([dict(artist=x['artist'], place=x['place'], state=x.get('state', ''), country=x.get('country', 'US'), lat=x['lat'], lon=x['lon'], source='Capy', whole_state=bool(x.get('whole_state')))])])
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
P['plays'] = P.artist.map(vc).fillna(0).astype(int); P = P[P.plays > 0]
P['lane'] = P.artist.map(la).fillna('No lane'); P['family'] = P.lane.map(fam).fillna('Other')
P['label'] = P.apply(lambda r: r.place if r.whole_state else r.place + (', ' + r.state if r.state else '') + ('' if r.country == 'US' else ', ' + r.country), axis=1)
P.sort_values('plays', ascending=False)[['artist', 'label', 'place', 'state', 'country', 'lat', 'lon', 'plays', 'lane', 'family', 'source']].to_csv('out/artist_places.csv', index=False)
rows = []
for lab, g in P.sort_values('plays', ascending=False).groupby('label', sort=False):
    rows.append(dict(label=lab, place=g.place.iloc[0], state=g.state.iloc[0], country=g.country.iloc[0], lat=g.lat.iloc[0], lon=g.lon.iloc[0], plays=int(g.plays.sum()),
                     artists=len(g), top_artist=g.artist.iloc[0], family=g.family.iloc[0], names=' | '.join(f'{a}:{n}' for a, n in zip(g.artist, g.plays))))
C = pd.DataFrame(rows).sort_values('plays', ascending=False); C.insert(0, 'rank', range(1, len(C) + 1))
C.to_csv('out/place_plays.csv', index=False)
top = vc.head(200); placed = set(P.artist)
K = [('placed_artists', len(P), 'Artists on the map'), ('places', len(C), 'Places'),
     ('top200_share', round(top[top.index.isin(placed)].sum() / top.sum(), 3), 'Share of your top 200 artists\' plays that are placed'),
     ('unplaced_top', ' | '.join(a for a in top.index if a not in placed)[:4000], 'Top 200 artists with no place yet')]
pd.DataFrame(K, columns=['metric', 'value', 'label']).to_csv('out/places_summary.csv', index=False)
print(C.head(12)[['rank', 'label', 'plays', 'artists', 'top_artist']].to_string(index=False)); print(K[:3])
