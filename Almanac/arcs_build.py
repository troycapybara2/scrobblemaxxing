# Artist arcs: the shape of each top artist's history, year by year.
# Shapes (checked in this order), on yearly plays with the current year at its pace so far:
# Burst: one year holds half the plays and only 3 years reach a tenth of the peak. Comeback: a strong run, 2+ quiet years
# (under 15% of peak), then strong again. Slow burn: peak in the last 3 years, 3+ years after starting, still near it.
# Evergreen: 7+ years at a tenth of the peak and still played (last 2 years 10%+ of peak). New era: arrived in the last
# 5 years and still going strong. Faded: last 2 years under a tenth of the peak. Else On and off.
# The current year counts as a full year at its pace so far.
import pandas as pd, numpy as np
df = pd.read_pickle('df_raw.pkl'); df['y'] = df.ts.dt.year
NOW = df.ts.max(); Y0, Y1 = int(df.y.min()), int(NOW.year)
frac = (NOW - pd.Timestamp(f'{Y1}-01-01', tz=NOW.tz)).days / 365.25
top = df.artist.value_counts().head(60).index
la = pd.read_csv('artist_lanes.csv').set_index('artist').lane
fam = dict(pd.read_csv('out/now_buckets.csv')[['bucket', 'family']].values)
rows = []
for a in top:
    s = df[df.artist == a].y.value_counts().reindex(range(Y0, Y1 + 1), fill_value=0).astype(float)
    s_pace = s.copy(); s_pace[Y1] = s[Y1] / max(frac, 0.1)
    pk = s_pace.max(); act = [y for y in s.index if s_pace[y] >= 0.1 * pk]; first = act[0]
    span = s_pace.loc[first:Y1]; peak_y = int(span.idxmax()); recent = span.iloc[-2:].mean() / pk
    hi = [y for y in span.index if span[y] >= 0.4 * pk]
    gap = any(span.get(y, 0) <= 0.15 * pk and span.get(y + 1, 0) <= 0.15 * pk for y in span.index if hi and hi[0] < y and y + 1 < hi[-1])
    if s.max() / s.sum() >= 0.5 and len(act) <= 3: arc = 'Burst'
    elif gap and len(hi) >= 2: arc = 'Comeback'
    elif peak_y >= Y1 - 2 and peak_y - first >= 3 and recent >= 0.4: arc = 'Slow burn'
    elif len(act) >= 7 and recent >= 0.1: arc = 'Evergreen'
    elif first >= Y1 - 5 and recent >= 0.25: arc = 'New era'
    elif recent < 0.1: arc = 'Faded'
    else: arc = 'On and off'
    rows.append(dict(artist=a, arc=arc, plays=int(s.sum()), peak_year=peak_y, peak_plays=int(s[peak_y]), first_year=first, last_strong_year=max(hi) if hi else peak_y, recent_share=round(float(recent), 3),
                     lane=la.get(a, 'Long tail'), family=fam.get(la.get(a, ''), 'Other'), years='|'.join(f'{y}:{int(n)}' for y, n in s.items())))
A = pd.DataFrame(rows); A['arc_order'] = A.arc.map({'Evergreen': 0, 'New era': 1, 'Slow burn': 2, 'Comeback': 3, 'On and off': 4, 'Burst': 5, 'Faded': 6})
A = A.sort_values(['arc_order', 'plays'], ascending=[True, False]).drop(columns='arc_order')
A.to_csv('out/artist_arcs.csv', index=False)
print(A.groupby('arc').artist.apply(lambda x: ', '.join(x[:8])).to_string())
