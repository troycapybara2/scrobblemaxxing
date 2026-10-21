import pandas as pd, numpy as np, collections, itertools, networkx as nx
from networkx.algorithms.community import louvain_communities
df=pd.read_pickle('df.pkl')
df['sess']=(df.uts.diff().fillna(1e9)>1800).cumsum()
E=df[df.ts>=pd.Timestamp('2023-01-01',tz='America/New_York')].copy()
vc=E.artist.value_counts()
TOP=list(vc.head(250).index)
S=E[E.artist.isin(TOP)].groupby('sess').artist.apply(set)
occ=collections.Counter(); pair=collections.Counter()
for s in S:
    for a in s: occ[a]+=1
    for a,b in itertools.combinations(sorted(s),2): pair[(a,b)]+=1
def jac(a,b):
    c=pair.get((a,b) if a<b else (b,a),0); return (c/(occ[a]+occ[b]-c) if c else 0),c
G=nx.Graph(); G.add_nodes_from(TOP)
for a,b in itertools.combinations(TOP,2):
    j,c=jac(a,b)
    if c>=4 and j>0.04: G.add_edge(a,b,weight=j)
