import networkx as nx, pandas as pd, numpy as np, collections, itertools, math
df=pd.read_pickle('df.pkl'); df['y']=df.ts.dt.year
vc=df.artist.value_counts(); TOP=list(vc[vc>=30].index); T=set(TOP)
# the day each artist reached 30 plays; recent ones are the newest arrivals
srt=df[df.artist.isin(T)].sort_values('ts'); srt['n']=srt.groupby('artist').cumcount()+1
CROSS=srt[srt.n==30].set_index('artist').ts
NOW=df.ts.max(); NEW_DAYS=60
sess=(df.uts.diff().fillna(1e9)>1800).cumsum()
S=pd.Series(df.artist.values,index=sess.values); S=S[S.isin(T)]
occ=collections.Counter(); pair=collections.Counter()
for s in S.groupby(level=0).apply(lambda s: frozenset(s)):
    for a in s: occ[a]+=1
    if len(s)<=60:
        for a,b in itertools.combinations(sorted(s),2): pair[(a,b)]+=1
g=nx.Graph(); g.add_nodes_from(TOP)
for (a,b),c in pair.items():
    if c<2: continue
    j=c/(occ[a]+occ[b]-c)
    if j>=0.015: g.add_edge(a,b,weight=j)
cs=nx.community.louvain_communities(g,weight='weight',resolution=4,seed=7)
cs=sorted(cs,key=lambda c:-sum(vc[a] for a in c))
big=[set(c) for c in cs if len(c)>=4]; small=[a for c in cs if len(c)<4 for a in c]
cid={a:i for i,c in enumerate(big) for a in c}
stray=[]
for a in small:
    w=collections.Counter()
    for b,d in g[a].items():
        if b in cid: w[cid[b]]+=d['weight']
    if w: cid[a]=w.most_common(1)[0][0]
    else: stray.append(a)
if stray:
    cid.update({a:len(big) for a in stray})
K=max(cid.values())+1
LANE=pd.read_csv('artist_lanes.csv').set_index('artist').lane
exec(open('lane_map.py').read().split('def build_lanes')[0])
mem=collections.defaultdict(list)
for a,c in cid.items(): mem[c].append(a)
# organic layout: one force layout for all 1,000 artists, with links inside a cluster pulling harder
H=nx.Graph(); H.add_nodes_from(g.nodes)
for a,b,d in g.edges(data=True):
    H.add_edge(a,b,weight=d['weight']*(8.0 if cid[a]==cid[b] else 0.15))
for c in range(K):  # a hidden hub per cluster keeps loose members near their crowd
    hub=f'__hub{c}'; H.add_node(hub)
    for a in mem[c]: H.add_edge(hub,a,weight=0.08)
import json, os
PREV='solar_positions.json'
init=None
if os.path.exists(PREV):
    old=json.load(open(PREV)); init={}
    for v in H.nodes:
        if v in old: init[v]=np.array(old[v])/1000
        elif not str(v).startswith('__hub'):
            nb=[old[b] for b in g[v] if b in old]
            init[v]=(np.mean(nb,axis=0)/1000 if nb else np.random.RandomState(0).uniform(-1,1,2))
    for c in range(K):
        mm=[init[a] for a in mem[c] if a in init]; init[f'__hub{c}']=np.mean(mm,axis=0) if mm else np.zeros(2)
pos=nx.spring_layout(H,weight='weight',seed=5,k=0.09,iterations=800 if init is None else 250,pos=init)
P={a:np.array(pos[a])*1000 for a in g.nodes}
json.dump({a:[float(P[a][0]),float(P[a][1])] for a in g.nodes},open(PREV,'w'))
nodes=[]; clusters=[]
first=df.groupby('artist').ts.min(); last=df.groupby('artist').ts.max()
toptr=df[df.artist.isin(T)].groupby(['artist','track']).size().reset_index().sort_values(0).drop_duplicates('artist',keep='last').set_index('artist')
for c in range(K):
    m=sorted(mem[c],key=lambda a:-vc[a]); n=len(m)
    lanes=collections.Counter()
    for a in m: lanes[LANE.get(a,'Long tail')]+=int(vc[a])
    lane=[l for l,_ in lanes.most_common() if l!='Long tail'][:1]; lane=lane[0] if lane else 'Long tail'
    fam=LANEFAM.get(lane,'Long tail')
    name=m[0] if c<len(big) else 'Deep space'
    gp=df[df.artist.isin(m)]; yr=gp.y.value_counts()
    cx=np.average([P[a][0] for a in m],weights=[vc[a] for a in m]); cy=np.average([P[a][1] for a in m],weights=[vc[a] for a in m])
    clusters.append(dict(id=c,name=name,lane=lane,family=fam,x=round(cx,1),y=round(cy,1),artists=n,plays=int(gp.shape[0]),
        peak_year=int(yr.idxmax()),plays_2026=int((gp.y==2026).sum()),members=', '.join(m[1:5])))
    for k2,a in enumerate(m):
        nodes.append(dict(artist=a,cluster=c,rank_in_cluster=k2+1,x=round(P[a][0],1),y=round(P[a][1],1)))
N=pd.DataFrame(nodes)
N['plays']=N.artist.map(vc).astype(int); N['lane']=N.artist.map(LANE).fillna('Long tail')
N['first_listen']=N.artist.map(first).dt.strftime('%Y-%m-%d'); N['last_listen']=N.artist.map(last).dt.strftime('%Y-%m-%d')
N['top_track']=N.artist.map(toptr.track); N['top_track_plays']=N.artist.map(toptr[0]).astype(int)
N['system']=N.cluster.map({c['id']:c['name'] for c in clusters})
N['crossed_30']=N.artist.map(CROSS).dt.strftime('%Y-%m-%d')
N['is_new']=N.artist.map(lambda a:'yes' if (NOW-CROSS[a]).days<=NEW_DAYS else 'no')
N.to_csv('out/solar_nodes.csv',index=False)
E=[]
for a in g.nodes:
    nb=sorted(g[a].items(),key=lambda kv:-kv[1]['weight'])[:6]
    for b,d in nb:
        E.append(dict(source=a,target=b,jaccard=round(d['weight'],3),shared_sessions=pair.get((a,b) if a<b else (b,a),0)))
pd.DataFrame(E).to_csv('out/solar_edges.csv',index=False)
C=pd.DataFrame(clusters)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def blob(c):
    m=N[N.cluster==c]; xs=m.x.values; ys=m.y.values; wts=np.sqrt(m.plays.values)
    bw=26.0; pad=3*bw
    gx=np.arange(xs.min()-pad,xs.max()+pad,5.0); gy=np.arange(ys.min()-pad,ys.max()+pad,5.0)
    X,Y=np.meshgrid(gx,gy); Z=np.zeros_like(X)
    for x0,y0,w0 in zip(xs,ys,wts): Z+=w0*np.exp(-((X-x0)**2+(Y-y0)**2)/(2*bw*bw))
    at=np.array([Z[np.abs(gy-y0).argmin(),np.abs(gx-x0).argmin()] for x0,y0 in zip(xs,ys)])
    lvl=max(np.percentile(at,8)*0.55,Z.max()*0.02)
    cs=plt.contour(X,Y,Z,levels=[lvl]); plt.close('all')
    parts=[]
    for path in cs.get_paths():
        for poly in path.to_polygons():
            if len(poly)<4: continue
            parts.append('M'+'L'.join(f'{p[0]:.0f},{p[1]:.0f}' for p in poly[::2])+'Z')
    return ''.join(parts)
C['shape']=[blob(c) for c in C.id]
C.to_csv('out/solar_systems.csv',index=False)
print(K,'systems'); print(C[['name','lane','artists','plays','peak_year','members']].to_string())
