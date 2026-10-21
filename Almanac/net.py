import pandas as pd, numpy as np, collections, itertools, networkx as nx, sys
from networkx.algorithms.community import louvain_communities
df=pd.read_pickle('df.pkl')
df['sess']=(df.uts.diff().fillna(1e9)>1800).cumsum()
vc=df.artist.value_counts()
TOPN=int(sys.argv[1]) if len(sys.argv)>1 else 200
top=list(vc.head(TOPN).index)
S=df[df.artist.isin(top)].groupby('sess').artist.apply(set)
occ=collections.Counter(); pair=collections.Counter()
for s in S:
    for a in s: occ[a]+=1
    for a,b in itertools.combinations(sorted(s),2): pair[(a,b)]+=1
G=nx.Graph()
for a in top: G.add_node(a)
for (a,b),c in pair.items():
    if c>=8:
        jac=c/(occ[a]+occ[b]-c)
        if jac>0.03: G.add_edge(a,b,weight=jac)
if __name__=='__main__':
  for res in [1.3,1.6]:
    comms=louvain_communities(G,weight='weight',seed=1,resolution=res)
    comms=sorted(comms,key=lambda c:-sum(vc[a] for a in c))
    print('RES',res)
    for c in comms:
        cs=sorted(c,key=lambda a:-vc[a]); 
        if len(c)>1: print(len(c), sum(vc[a] for a in c), cs[:22]); print()
