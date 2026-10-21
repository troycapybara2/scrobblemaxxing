import pandas as pd, numpy as np, collections, itertools
df=pd.read_pickle('df.pkl')
df['sess']=(df.uts.diff().fillna(1e9)>1800).cumsum()
df['mon']=df.ts.dt.strftime('%Y-%m')
vc=df.artist.value_counts(); TOP=list(vc.head(400).index); T=set(TOP)
S=df[df.artist.isin(T)].groupby('sess').agg(arts=('artist',lambda s:frozenset(s)),mon=('mon','first'))
ns=len(S)
occ=collections.Counter(); pair=collections.Counter()
mon_n=S.groupby('mon').size()
mon_occ=collections.defaultdict(collections.Counter)  # month -> artist -> sessions
for arts,m in zip(S.arts,S.mon):
    for a in arts: occ[a]+=1; mon_occ[m][a]+=1
    for a,b in itertools.combinations(sorted(arts),2): pair[(a,b)]+=1
# sessions per artist by month
art_mon=collections.defaultdict(collections.Counter)
for m,c in mon_occ.items():
    for a,n in c.items(): art_mon[a][m]=n
def shared(a,b): return pair.get((a,b) if a<b else (b,a),0)
def expected(b,a):
    # if a appeared in sessions at its usual rate *in the same months* b was played
    return sum(n*mon_occ[m][a]/mon_n[m] for m,n in art_mon[b].items())
def stats(b,a):
    c=shared(a,b)
    if c==0: return None
    e=expected(b,a)
    jac=c/(occ[a]+occ[b]-c)
    return dict(neighbor=a,shared=c,jaccard=jac,expected=e,lift=(c+1)/(e+1))
