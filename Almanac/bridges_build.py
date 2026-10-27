# Bridge artists: who links two clusters of the galaxy. Uses the galaxy's own clusters and co-listening links (solar_build.py).
# For each artist, link strength = summed Jaccard of its links into each cluster. A bridge has real pull into a cluster
# besides its own (at least half its home strength). score = sqrt(home x other), x1.5 when the two clusters sit in
# different lane families, scaled down for artists under 1,000 plays. Run after solar_build.py.
import pandas as pd, numpy as np, collections
N = pd.read_csv('out/solar_nodes.csv'); E = pd.read_csv('out/solar_edges.csv'); SY = pd.read_csv('out/solar_systems.csv')
cl = dict(zip(N.artist, N.system)); pl = dict(zip(N.artist, N.plays)); fam = dict(zip(SY.name, SY.family))
W = collections.defaultdict(lambda: collections.defaultdict(float)); NB = collections.defaultdict(dict)
for s, t, j, n in E[['source', 'target', 'jaccard', 'shared_sessions']].drop_duplicates().itertuples(index=False):
    if s not in cl or t not in cl or s == t: continue
    for a, b in ((s, t), (t, s)):
        if b in NB[a]: continue
        NB[a][b] = (j, n); W[a][cl[b]] += j
rows = []
for a, d in W.items():
    own = d.get(cl[a], 0); oth = {k: v for k, v in d.items() if k != cl[a]}
    if not oth or own == 0 or pl[a] < 75: continue
    k, v = max(oth.items(), key=lambda x: x[1])
    if v < 0.5 * own: continue
    cross = fam.get(cl[a]) != fam.get(k)
    score = np.sqrt(own * v) * (1.5 if cross else 1) * min(1, np.log10(pl[a]) / 3)
    top = lambda c: sorted(((jj, b, nn) for b, (jj, nn) in NB[a].items() if cl[b] == c), reverse=True)[:3]
    rows.append(dict(artist=a, plays=int(pl[a]), home=cl[a], home_family=fam.get(cl[a], ''), other=k, other_family=fam.get(k, ''),
                     across_families='yes' if cross else 'no', score=round(score, 3),
                     via_home=' | '.join(f'{b}:{nn}' for _, b, nn in top(cl[a])), via_other=' | '.join(f'{b}:{nn}' for _, b, nn in top(k))))
R = pd.DataFrame(rows).sort_values('score', ascending=False).head(40)
R.insert(0, 'rank', range(1, len(R) + 1))
R.to_csv('out/bridges.csv', index=False)
print(R.head(15)[['rank', 'artist', 'plays', 'home', 'other', 'across_families', 'via_home', 'via_other']].to_string(index=False))
