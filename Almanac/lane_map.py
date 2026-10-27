# Capy's lanes for every artist across the whole history.
import pandas as pd, numpy as np, collections, itertools
_src=open('buckets6.py').read(); _i=_src.index('B={'); _j=_src.index("sub={a:k"); _ns={}; exec(_src[_i:_j],_ns)
LB=_ns['B']
U='Underground & rap'; P='Pop, R&B & country'; EM='Emo & indie'; C='Classics'; OT='Other'
LANEFAM={'Michigan':U,'Underground':U,'SoundCloud':U,'Mainstream':U,'R&B':P,'Alt rap':U,'West coast':U,'Female rap':U,'The new wave (2025–26)':U,'Hyperpop':U,
 'Pop':P,'Country & folk':P,'Emo revival 2.0':EM,'DIY emo':EM,'EDM':'EDM','Indie emo':EM,'Indie':EM,'Emo revival 1.0':EM,'Warped Tour pop punk (2010s)':EM,'Scene kid (2000s)':EM,'Folk punk':EM,'Hardcore':EM,
 'Old rock appreciation':C,'Appreciating the greats':C,'Old rap':C,'Blog-era nostalgia':C,'Grab bag':OT,'TikTok one-hit wonders':OT,'Instrumental':OT}
LSEED={a:k for k,v in LB.items() for a in v.split('|')}
def build_lanes(df):
    sess=(df.uts.diff().fillna(1e9)>1800).cumsum()
    vc=df.artist.value_counts(); cand=set(vc[vc>=25].index)
    S=pd.Series(df.artist.values,index=sess.values).groupby(level=0).apply(lambda s:set(s)&(cand|set(LSEED)))
    occ=collections.Counter(); pair=collections.Counter()
    for s in S:
        for a in s: occ[a]+=1
        for a,b in itertools.combinations(sorted(s),2): pair[(a,b)]+=1
    lane={a:k for a,k in LSEED.items() if a in vc.index}; how={a:'you' for a in lane}
    for a in cand-set(lane):
        sc=collections.defaultdict(list)
        for b,k in list(lane.items()):
            if how.get(b)!='you' or b not in occ: continue
            c=pair.get((a,b) if a<b else (b,a),0)
            if c: sc[k].append(c/(occ[a]+occ[b]-c))
        if not sc: continue
        best=max(sc,key=lambda k:np.mean(sorted(sc[k],reverse=True)[:3]))
        m={k:np.mean(sorted(v,reverse=True)[:3]) for k,v in sc.items()}; o=sorted(m.values(),reverse=True)
        if o[0]>=0.10 and (len(o)==1 or o[0]>=1.5*o[1]): lane[a]=best; how[a]='co-listening'
    return lane,how
