import pandas as pd, numpy as np, collections, itertools, re, json, os
import networkx as nx
from networkx.algorithms.community import louvain_communities
from load import load_lb
OUT='out'; os.makedirs(OUT,exist_ok=True)
df=pd.read_pickle('df.pkl')
df['y']=df.ts.dt.year
df['sess']=(df.uts.diff().fillna(1e9)>1800).cumsum()
NOW=df.ts.max(); BASE=pd.Timestamp('2025-12-09 21:16:08',tz='UTC')
vc=df.artist.value_counts()
def save(name,d):
    d.to_csv(f'{OUT}/{name}.csv',index=False); print(name,len(d))
def ranks(sub):
    g=sub.groupby('artist').agg(n=('uts','size'),last=('uts','max')).sort_values(['n','last'],ascending=[False,True])
    g['rank']=np.arange(1,len(g)+1); return g
R_now=ranks(df); R_base=ranks(df[df.ts<BASE])

# ---------- scenes ----------
top200=list(vc.head(200).index)
S=df[df.artist.isin(vc.head(1000).index)].groupby('sess').artist.apply(set)
occ=collections.Counter(); pair=collections.Counter()
for s in S:
    for a in s: occ[a]+=1
    for a,b in itertools.combinations(sorted(s),2): pair[(a,b)]+=1
def jac(a,b):
    c=pair.get((a,b) if a<b else (b,a),0); return c/(occ[a]+occ[b]-c) if c else 0, c
G=nx.Graph(); G.add_nodes_from(top200)
for a,b in itertools.combinations(top200,2):
    j,c=jac(a,b)
    if c>=8 and j>0.03: G.add_edge(a,b,weight=j)
comms=louvain_communities(G,weight='weight',seed=1,resolution=1.6)
comms=sorted([c for c in comms if len(c)>2],key=lambda c:-sum(vc[a] for a in c))
NAMES={'Hoodie Allen':'Blog-Era & Big Rap','Mom Jeans.':'Emo Revival & Indie','Lil Uzi Vert':'SoundCloud Rap',
 'Real Friends':'Pop-Punk & Emo Class of 2016','DJ Lucas':'Underground & Plugg','Panic! at the Disco':'Warped Tour Years','Taylor Swift':'Pop & R&B'}
scene={}
for c in comms:
    _ref=pd.read_csv('ref_top500_scenes.csv').set_index('artist').scene
    _v=collections.Counter()
    for a in c: _v[_ref.get(a,'?')]+=vc[a]
    _v.pop('?',None); _v.pop('Long tail',None)
    nm=_v.most_common(1)[0][0] if _v else None
    if not nm: continue
    for a in c: scene[a]=nm
# assign 201-1000 by affinity
core=dict(scene)
for a in vc.head(1000).index:
    if a in scene: continue
    sc=collections.Counter()
    for b,s in core.items():
        j,c=jac(a,b)
        if c>=3: sc[s]+=j
    if sc and sc.most_common(1)[0][1]>=0.04: scene[a]=sc.most_common(1)[0][0]
exec(open('lane_map.py').read())
LANE,LANEHOW=build_lanes(df)
scene=dict(LANE)
FAM_ORDER=['Emo & indie','Underground & rap','Pop, R&B & country','EDM','Classics','Other','Long tail']
df['scene']=df.artist.map(scene).fillna('Long tail')
df['family']=df.scene.map(LANEFAM).fillna('Long tail')
pd.DataFrame([dict(artist=a,lane=l,how=LANEHOW[a]) for a,l in LANE.items()]).to_csv('artist_lanes.csv',index=False)
print('scene coverage', (df.scene!='Long tail').mean())
print(df.groupby('scene').size())

# ---------- kpis ----------
d365=df[df.ts>NOW-pd.Timedelta(days=365)]
k=[('total_scrobbles',len(df),'Total scrobbles'),('unique_artists',df.artist.nunique(),'Artists'),
   ('unique_albums',df[df.album!=''].groupby(['artist','album']).ngroups,'Albums'),
   ('unique_tracks',df.groupby(['artist','track']).ngroups,'Tracks'),
   ('years',round((NOW-df.ts.min()).days/365.25,1),'Years of history'),
   ('days_with_music',df.ts.dt.date.nunique(),'Days with a scrobble'),
   ('per_day_365',round(len(d365)/365,1),'Scrobbles per day, last 365 days'),
   ('first_scrobble',df.ts.min().strftime('%Y-%m-%d'),'First scrobble'),
   ('last_scrobble',NOW.strftime('%Y-%m-%d'),'Latest scrobble'),
   ('app_start',BASE.tz_convert('America/New_York').strftime('%Y-%m-%d'),'Leaderboard app launched'),
   ('top500_cutoff_now',int(R_now.iloc[499].n),'Plays needed for top 500 now'),
   ('top500_cutoff_base',int(R_base.iloc[499].n),'Plays needed for top 500 at app launch'),
   ('plays_since_base',int((df.ts>=BASE).sum()),'Scrobbles since app launch'),
   ('hoodie_uzi_gap',int(R_now.loc['Hoodie Allen','n']-R_now.loc['Lil Uzi Vert','n']),'Plays between #1 and #2'),
   ('sessions',df.sess.nunique(),'Listening sessions'),
]
save('kpis',pd.DataFrame(k,columns=['metric','value','label']))

# ---------- monthly ----------
df['month']=df.ts.dt.strftime('%Y-%m')
m=df.groupby('month').agg(scrobbles=('uts','size'),artists=('artist','nunique')).reset_index()
ta=df.groupby(['month','artist']).size().reset_index(name='n').sort_values(['month','n'],ascending=[True,False]).drop_duplicates('month')
m=m.merge(ta.rename(columns={'artist':'top_artist','n':'top_artist_plays'}),on='month')
save('monthly',m)

# ---------- yearly ----------
first_year=df.groupby('artist').y.min()
rows=[]
for y,g in df.groupby('y'):
    a=g.artist.value_counts(); al=g[g.album!=''].groupby(['artist','album']).size().sort_values(ascending=False)
    tr=g.groupby(['artist','track']).size().sort_values(ascending=False)
    h=g.ts.dt.hour
    rows.append(dict(year=y,scrobbles=len(g),artists=g.artist.nunique(),new_artists=int((first_year==y).sum()),
      per_day=round(len(g)/g.ts.dt.date.nunique(),1),top_artist=a.index[0],top_artist_plays=int(a.iloc[0]),
      top_album=al.index[0][1],top_album_artist=al.index[0][0],top_album_plays=int(al.iloc[0]),
      top_track=tr.index[0][1],top_track_artist=tr.index[0][0],top_track_plays=int(tr.iloc[0]),
      top10_share=round(a.head(10).sum()/len(g),3),night_share=round(((h>=22)|(h<4)).mean(),3),
      peak_hour=int(h.mode()[0]),top_scene=g[g.scene!='Long tail'].scene.value_counts().index[0],
      partial=('yes' if y in (2011,2026) else 'no')))
save('yearly',pd.DataFrame(rows))

# ---------- eras ----------
eras=[
 ('Scene kid','2011-07','2012-05','Warped Tour Years','Attack Attack!, I See Stars, Hoodie Allen\'s Leap Year and Pep Rally mixtapes, T. Mills. Crabcore and blog rap share a playlist.'),
 ('The Hoodie Allen years','2012-06','2014-12','Blog-Era & Big Rap','Hoodie Allen tops every single year from 2011 through 2014, with Childish Gambino, G-Eazy and OCD: Moosh & Twist close behind. Crew Cuts gets 482 plays in 2013 alone.'),
 ('Trap breaks open','2015-01','2015-12','Blog-Era & Big Rap','Fetty Wap, Young Thug, Future and Drake take over. Listening volume nearly doubles as the library goes from 416 artists in 2014 to 701.'),
 ('Pop-punk summer','2016-01','2016-12','Pop-Punk & Emo Class of 2016','The busiest year on record. Real Friends gets 1,982 plays, blackbear 1,410, The Front Bottoms 889. Weak When Ur Around plays 65 times in one day.'),
 ('SoundCloud takeover','2017-01','2018-12','SoundCloud Rap','Lil Uzi Vert arrives and never leaves. Carti, Ski Mask, XXXTENTACION, NAV, Trippie Redd, PnB Rock. Mom Jeans. runs alongside as the emo counterweight.'),
 ('Emo revival','2019-01','2020-12','Emo Revival & Indie','Origami Angel and Prince Daddy & The Hyena own 2019. Eternal Atake owns 2020. The night-owl era ends here: late-night share drops from 22% to 12%.'),
 ('The BabyTron year','2021-01','2021-12','Michigan','Michigan arrives: BabyTron (582 plays), YN Jay and ShittyBoyz. Pi\'erre Bourne is your #2 artist of the year (468), but he stays on the SoundCloud side next to Uzi.'),
 ('Sweet Tooth','2022-01','2022-12','Emo Revival & Indie','Mom Jeans. drops Sweet Tooth (489 plays) and Hot Mulligan, The Story So Far and oso oso pull emo back to the top for one more year.'),
 ('Wide open','2023-01','2026-10','Underground & Plugg','The most spread-out stretch of the library. Your top 10 artists take about a fifth of each year\'s plays, down from 70% in 2013. RTB MB, DJ Lucas, Bladee, Alex G, SZA and Paul trade the top spot.'),
]
_er=pd.DataFrame(eras,columns=['era','start','end','scene','story'])
_ERA_LANE={'Scene kid':'Scene kid (2000s)','The Hoodie Allen years':'Blog-era nostalgia','Trap breaks open':'Mainstream','Pop-punk summer':'Warped Tour pop punk (2010s)','SoundCloud takeover':'SoundCloud','Emo revival':'Midwest emo','The BabyTron year':'Michigan','Sweet Tooth':'Midwest emo','Wide open':'Michigan'}
_er['scene']=_er.era.map(_ERA_LANE)
save('eras',_er)

# ---------- top-500 race since app launch ----------
pre=df[df.ts<BASE]; post=df[df.ts>=BASE]
cnt=collections.Counter(pre.artist); lastreach=pre.groupby('artist').uts.max().to_dict()
t0=set(R_base.index[:500]); inset=set(t0); entries=collections.defaultdict(list); exits=collections.defaultdict(list)
freq=collections.Counter(cnt.values())
for r in post.itertuples():
    a=r.artist; old=cnt[a]
    if old: freq[old]-=1
    cnt[a]=old+1; freq[old+1]+=1; lastreach[a]=r.uts; c=old+1
    rank=sum(v for kk,v in freq.items() if kk>=c)
    if rank<=500 and a not in inset:
        inset.add(a); entries[a].append(r.ts)
        if len(inset)>500:
            low=min(inset,key=lambda x:(cnt[x],-lastreach[x])); inset.remove(low); exits[low].append(r.ts)
# app log
objs=load_lb(); applog={}
for o in objs[1:]:
    for a,v in o.get('data',{}).items():
        if v.get('rank') and v['rank']<=500: applog.setdefault(a,o['timestamp'][:10])
fe=df.groupby('artist').ts.min()
rows=[]
for a in entries:
    if a in t0: continue
    g=post[post.artist==a]; tt=g.track.value_counts()
    rows.append(dict(artist=a,entered=entries[a][0].strftime('%Y-%m-%d'),plays_at_launch=int(R_base.n.get(a,0)),
        rank_at_launch=int(R_base['rank'].get(a,0)) or None,plays_now=int(R_now.loc[a,'n']),rank_now=int(R_now.loc[a,'rank']),
        plays_since_launch=len(g),status=('In top 500' if a in R_now.index[:500] else 'Dropped back out'),
        times_entered=len(entries[a]),first_ever_listen=fe[a].strftime('%Y-%m-%d'),top_track_since=tt.index[0],
        top_track_plays=int(tt.iloc[0]),scene=scene.get(a,'Long tail'),
        app_logged=applog.get(a,'after app stopped' if entries[a][0]>pd.Timestamp('2026-09-23',tz='UTC') else 'not logged')))
ent=pd.DataFrame(rows).sort_values('entered'); save('top500_entrants',ent)
# movers for current top 500
mv=R_now.head(500).copy()
mv['rank_launch']=R_base['rank'].reindex(mv.index)
mv['plays_launch']=R_base.n.reindex(mv.index).fillna(0).astype(int)
mv=mv.reset_index().rename(columns={'n':'plays','rank':'rank_now'})
mv['places_moved']=(mv.rank_launch-mv.rank_now)
mv['plays_since_launch']=mv.plays-mv.plays_launch
mv['scene']=mv.artist.map(scene).fillna('Long tail')
mv['first_listen']=mv.artist.map(fe).dt.strftime('%Y-%m-%d')
mv['last_listen']=mv.artist.map(df.groupby('artist').ts.max()).dt.strftime('%Y-%m-%d')
mv['rank_launch']=mv.rank_launch.astype('Int64'); mv['places_moved']=mv.places_moved.astype('Int64')
save('top500_now',mv[['artist','rank_now','plays','rank_launch','plays_launch','places_moved','plays_since_launch','scene','first_listen','last_listen']])

# ---------- projections ----------
def rate(days): return df[df.ts>NOW-pd.Timedelta(days=days)].artist.value_counts()
r90,r180,r365=rate(90),rate(180),rate(365)
P=pd.DataFrame({'plays':vc}).join(pd.DataFrame({'d90':r90,'d180':r180,'d365':r365})).fillna(0)
P['per_day']=0.5*P.d90/90+0.3*P.d180/180+0.2*P.d365/365
P['proj']=(P.plays+P.per_day*365).round().astype(int)
P['rank_now']=R_now['rank'].reindex(P.index)
P=P.sort_values(['proj','plays'],ascending=False); P['rank_proj']=np.arange(1,len(P)+1)
pt=P.head(40).reset_index().rename(columns={'index':'artist'})
pt['plays_per_month']=(pt.per_day*30.44).round(1)
pt=pt[['artist','rank_now','plays','plays_per_month','proj','rank_proj']].rename(columns={'proj':'plays_oct_2027','rank_proj':'rank_oct_2027'})
pt['rank_change']=pt.rank_now-pt.rank_oct_2027
save('projection_top',pt)
# entrants projected
cut_proj=int(P.iloc[499].proj)
pe=P[(P.rank_proj<=500)&(P.rank_now>500)].reset_index().rename(columns={'index':'artist'})
def eta(row,cut):
    if row.per_day<=0: return None
    need=cut-row.plays
    if max(0,need)/row.per_day>36500: return None  # >100 years out: no date
    return (NOW+pd.Timedelta(days=max(0,need)/row.per_day)).strftime('%Y-%m-%d')
cut_now=int(R_now.iloc[499].n)
cand=P[(P.rank_now>500)&(P.per_day>0)].reset_index().rename(columns={'index':'artist'})
cand['plays_per_month']=(cand.per_day*30.44).round(1)
cand['plays_needed']=(cut_now+1-cand.plays).clip(lower=0).astype(int)
cand['eta']=cand.apply(lambda r: eta(r,cut_now+1),axis=1)
cand['projected_in']=cand.rank_proj<=500
cand=cand.sort_values('eta').head(25)
cand['scene']=cand.artist.map(scene).fillna('Long tail')
save('projection_entrants',cand[['artist','rank_now','plays','plays_needed','plays_per_month','eta','rank_proj','scene']].rename(columns={'rank_proj':'rank_oct_2027'}))
# race hoodie vs uzi
h=df[df.artist=='Hoodie Allen'].set_index('ts').uts; u=df[df.artist=='Lil Uzi Vert'].set_index('ts').uts
wk=pd.date_range('2016-03-06',NOW.tz_convert(None),freq='W-SUN',tz='America/New_York')
hc=np.searchsorted(h.index.values,wk.values,side='right'); uc=np.searchsorted(u.index.values,wk.values,side='right')
race=pd.DataFrame({'week':wk.strftime('%Y-%m-%d'),'hoodie':hc,'uzi':uc,'kind':'actual'})
hr=P.loc['Hoodie Allen','per_day']; ur=P.loc['Lil Uzi Vert','per_day']
lo=P.loc['Lil Uzi Vert','d365']/365; hi=P.loc['Lil Uzi Vert','d90']/90
gap=int(R_now.loc['Hoodie Allen','n']-R_now.loc['Lil Uzi Vert','n'])
fut=pd.date_range(wk[-1]+pd.Timedelta(days=7),periods=40,freq='W-SUN',tz='America/New_York')
dd=np.array([(f-NOW).days for f in fut])
H0=R_now.loc['Hoodie Allen','n']; U0=R_now.loc['Lil Uzi Vert','n']
race=pd.concat([race,pd.DataFrame({'week':fut.strftime('%Y-%m-%d'),'hoodie':(H0+hr*dd).round(1),'uzi':(U0+ur*dd).round(1),
   'uzi_low':(U0+lo*dd).round(1),'uzi_high':(U0+hi*dd).round(1),'kind':'projected'})])
save('race',race)
def cross(r): return (NOW+pd.Timedelta(days=(gap+1)/(r-hr))).strftime('%Y-%m-%d')
racek=pd.DataFrame([('hoodie_plays',int(H0)),('uzi_plays',int(U0)),('gap',gap),('uzi_per_month',round(ur*30.44,1)),('hoodie_per_month',round(hr*30.44,1)),
  ('eta_mid',cross(ur)),('eta_fast',cross(hi)),('eta_slow',cross(lo)),('hoodie_years_at_1',int(NOW.year-2011)),('uzi_first',fe['Lil Uzi Vert'].strftime('%Y-%m-%d')),('hoodie_last_play',df[df.artist=='Hoodie Allen'].ts.max().strftime('%Y-%m-%d'))],columns=['metric','value'])
save('race_facts',racek)
# milestones
tot=len(df); per=len(d365)/365
ms=[]
for mnum in [1,1000,10000,25000,50000,75000,100000,125000,150000]:
    r=df.iloc[mnum-1]; ms.append(dict(milestone=mnum,date=r.ts.strftime('%Y-%m-%d'),artist=r.artist,track=r.track,kind='reached'))
for mnum in [175000,200000,250000]:
    ms.append(dict(milestone=mnum,date=(NOW+pd.Timedelta(days=(mnum-tot)/per)).strftime('%Y-%m-%d'),artist='',track='',kind='projected'))
save('milestones',pd.DataFrame(ms))

# ---------- bump charts ----------
snaps=[(str(y),df[df.ts<pd.Timestamp(f'{y+1}-01-01',tz='America/New_York')]) for y in range(2011,2026)]
rk={lab:ranks(s)['rank'] for lab,s in snaps}; rk['Now']=R_now['rank']; rk['Oct 2027 (proj.)']=P.rank_proj
ever=set()
for lab,r in rk.items(): ever|=set(r[r<=10].index)
rows=[]
for lab,r in rk.items():
    for a in ever: rows.append(dict(snapshot=lab,artist=a,rank=int(r.get(a)) if a in r.index else None))
save('bump_alltime',pd.DataFrame(rows))
# annual
ann={y:g.artist.value_counts() for y,g in df.groupby('y')}
ever=set()
for y,v in ann.items(): ever|=set(v.index[:5])
rows=[]
for y,v in ann.items():
    rr=pd.Series(np.arange(1,len(v)+1),index=v.index)
    for a in ever: rows.append(dict(year=y,artist=a,rank=int(rr[a]) if a in rr.index else None,plays=int(v.get(a,0))))
save('bump_annual',pd.DataFrame(rows))

# ---------- scenes over time ----------
df['quarter']=df.ts.dt.year.astype(str)+'-Q'+df.ts.dt.quarter.astype(str)
sq=df.groupby(['quarter','family']).size().unstack(fill_value=0).reindex(columns=FAM_ORDER,fill_value=0).reset_index()
save('scenes_quarterly',sq)
# network: top 90 core
N90=[a for a in vc.head(110).index if a in core][:90]
H=G.subgraph(N90).copy()
pos=nx.spring_layout(H,weight='weight',seed=7,k=0.45,iterations=300)
nodes=pd.DataFrame([dict(artist=a,scene=scene.get(a,'Long tail'),plays=int(vc[a]),x=round(pos[a][0],4),y=round(pos[a][1],4)) for a in N90])
save('scene_nodes',nodes)
E=[]
for a,b,w in H.edges(data='weight'):
    j,c=jac(a,b)
    if j>=0.05: E.append(dict(source=a,target=b,jaccard=round(j,3),shared_sessions=c))
save('scene_edges',pd.DataFrame(E).sort_values('jaccard',ascending=False))
scn=[]
LANE_ORDER=list(df[df.scene!='Long tail'].scene.value_counts().index)+['Long tail']
for s in LANE_ORDER:
    g=df[df.scene==s]
    yr=g.groupby('y').size()
    scn.append(dict(scene=s,family=LANEFAM.get(s,'Long tail'),plays=len(g),share=round(len(g)/len(df),3),artists=int(g.artist.nunique()),
       peak_year=int(yr.idxmax()),peak_year_plays=int(yr.max()),leaders=', '.join(g.artist.value_counts().index[:5]),
       share_last_365=round((d365.artist.map(scene).fillna('Long tail')==s).mean(),3)))
pd.DataFrame([dict(lane=r['scene'],family=r['family'],plays=r['plays'],order=i+1) for i,r in enumerate(scn)]).to_csv(OUT+'/lanes.csv',index=False)
save('scenes',pd.DataFrame(scn))

# ---------- artist profiles (top 200) ----------
TOP=list(vc.head(200).index)
pf=[]; tr_rows=[]; nb_rows=[]; mon_rows=[]
for a in TOP:
    g=df[df.artist==a]; i=g.index[0]
    prev=df.artist.iloc[i-1] if i>0 and df.sess.iloc[i-1]==df.sess.iloc[i] else ''
    yr=g.groupby('y').size(); al=g[g.album!=''].album.value_counts(); tt=g.track.value_counts()
    pf.append(dict(artist=a,rank=int(R_now.loc[a,'rank']),plays=len(g),scene=scene.get(a,'Long tail'),
      first_listen=g.ts.min().strftime('%Y-%m-%d'),first_track=g.track.iloc[0],came_after=prev,
      last_listen=g.ts.max().strftime('%Y-%m-%d'),peak_year=int(yr.idxmax()),peak_year_plays=int(yr.max()),
      peak_share=round(yr.max()/len(g),3),years_active=int((yr>=10).sum()),
      top_album=al.index[0] if len(al) else '',top_album_plays=int(al.iloc[0]) if len(al) else 0,
      top_track=tt.index[0],top_track_plays=int(tt.iloc[0]),last_365=int(r365.get(a,0)),
      plays_per_month_now=round(P.loc[a,'per_day']*30.44,1),rank_oct_2027=int(P.loc[a,'rank_proj'])))
    for j,(t,n) in enumerate(tt.head(8).items()): tr_rows.append(dict(artist=a,track=t,plays=int(n),pos=j+1))
    sc=[]
    for b in vc.head(400).index:
        if b==a: continue
        jj,c=jac(a,b)
        if c>=5: sc.append((jj,c,b))
    for jj,c,b in sorted(sc,reverse=True)[:6]: nb_rows.append(dict(artist=a,neighbor=b,jaccard=round(jj,3),shared_sessions=c))
    for mo,n in g.groupby('month').size().items(): mon_rows.append(dict(artist=a,month=mo,plays=int(n)))
save('artist_profile',pd.DataFrame(pf)); save('artist_tracks',pd.DataFrame(tr_rows))
save('artist_neighbors',pd.DataFrame(nb_rows)); save('artist_monthly',pd.DataFrame(mon_rows))

# ---------- features ----------
low={a.lower():a for a in vc.head(300).index if len(a)>=4}
pat=re.compile(r'(?:feat\.?|ft\.?|featuring|\(with)\s+([^\)\]]+)',re.I)
links=collections.Counter(); ex={}
for (art,trk),n in df.groupby(['artist','track']).size().items():
    mm=pat.search(trk)
    if not mm: continue
    guests=mm.group(1).lower()
    for gl,gg in low.items():
        if gg!=art and re.search(r'(^|[\s,&])'+re.escape(gl)+r'($|[\s,&\)])',guests):
            links[(art,gg)]+=n; ex.setdefault((art,gg),[]).append((n,trk))
fl=[dict(host=a,guest=g,plays=n,top_track=max(ex[(a,g)])[1],host_rank=int(R_now.loc[a,'rank']),guest_rank=int(R_now.loc[g,'rank'])) for (a,g),n in links.most_common(40)]
save('feature_links',pd.DataFrame(fl))
df['guests']=df.track.str.extract(r'(?i)(?:feat\.?|ft\.?|featuring|\(with)\s+(.+)$')[0].str.lower().fillna('')
gdf=df[df.guests!='']; own=df.groupby('artist').ts.min(); gw=[]
for a in vc.head(150).index:
    if len(a)<4 or a in ('Paul','Watsky'): continue
    mm=gdf[(gdf.artist!=a)&gdf.guests.str.contains(r'(?:^|[\s,&])'+re.escape(a.lower())+r'(?:$|[\s,&\)\]])',regex=True)]
    if len(mm) and mm.ts.min()<own[a]-pd.Timedelta(days=1):
        r=mm.iloc[0]; gw.append(dict(artist=a,heard_on=r.artist,track=r.track,heard_date=r.ts.strftime('%Y-%m-%d'),own_first=own[a].strftime('%Y-%m-%d'),days_later=(own[a]-r.ts).days,rank_now=int(R_now.loc[a,'rank'])))
save('feature_gateways',pd.DataFrame(gw).sort_values('rank_now'))

# ---------- albums & tracks ----------
alb=df[df.album!=''].groupby(['artist','album']).agg(plays=('uts','size'),first=('ts','min'),last=('ts','max')).reset_index().sort_values('plays',ascending=False).head(50)
best=[]
for _,r in alb.iterrows():
    g=df[(df.artist==r.artist)&(df.album==r.album)]
    s=pd.Series(1,index=pd.to_datetime(g.uts,unit='s')).rolling('7D').sum()
    best.append((int(s.max()),s.idxmax().tz_localize('UTC').tz_convert('America/New_York').strftime('%Y-%m-%d')))
alb['best_week']=[b[0] for b in best]; alb['best_week_ending']=[b[1] for b in best]
alb['first']=alb['first'].dt.strftime('%Y-%m-%d'); alb['last']=alb['last'].dt.strftime('%Y-%m-%d')
alb['key']=alb.artist+' — '+alb.album
save('top_albums',alb[['key','artist','album','plays','first','last','best_week','best_week_ending']])
trk=df.groupby(['artist','track']).agg(plays=('uts','size'),first=('ts','min'),days=('ts',lambda s:s.dt.date.nunique())).reset_index().sort_values('plays',ascending=False).head(50)
trk['first']=trk['first'].dt.strftime('%Y-%m-%d'); trk['key']=trk.artist+' — '+trk.track
save('top_tracks',trk[['key','artist','track','plays','days','first']])
df['d']=df.ts.dt.strftime('%Y-%m-%d')
rep=df.groupby(['d','artist','track']).size().reset_index(name='plays').sort_values('plays',ascending=False).head(25)
rep['key']=rep.d+' '+rep.artist+' — '+rep.track
save('repeat_days',rep.rename(columns={'d':'date'})[['key','date','artist','track','plays']])
# comebacks
cb=[]
for a in vc.head(300).index:
    g=df[df.artist==a]; days=pd.to_datetime(pd.Series(sorted(g.d.unique())))
    gaps=days.diff().dt.days
    if len(gaps)<2: continue
    i=gaps.idxmax(); ret=days[i]
    after=g[(pd.to_datetime(g.d)>=ret)&(pd.to_datetime(g.d)<ret+pd.Timedelta(days=60))]
    if gaps[i]>=300 and len(after)>=25:
        cb.append(dict(artist=a,gap_days=int(gaps[i]),last_before=days[i-1].strftime('%Y-%m-%d'),returned=ret.strftime('%Y-%m-%d'),plays_next_60_days=len(after),return_track=after.track.value_counts().index[0]))
save('comebacks',pd.DataFrame(cb).sort_values('gap_days',ascending=False).head(15))

# ---------- habits ----------
df['dow']=df.ts.dt.dayofweek; df['hour']=df.ts.dt.hour
save('clock',df.groupby(['dow','hour']).size().reset_index(name='plays'))
era_bins=[(2011,2014,'2011–14'),(2015,2018,'2015–18'),(2019,2022,'2019–22'),(2023,2026,'2023–26')]
rows=[]
for a,b,lab in era_bins:
    g=df[(df.y>=a)&(df.y<=b)]; hh=g.hour.value_counts(normalize=True)
    for hr_ in range(24): rows.append(dict(period=lab,hour=hr_,share=round(hh.get(hr_,0),4)))
save('clock_by_period',pd.DataFrame(rows))
dd_=df.groupby('d').size()
busy=dd_.sort_values(ascending=False).head(10).reset_index(name='plays').rename(columns={'d':'date'})
busy['top_artist']=[df[df.d==x].artist.value_counts().index[0] for x in busy.date]
save('busiest_days',busy)
# streak
alld=pd.to_datetime(pd.Series(dd_.index))
run=(alld.diff().dt.days!=1).cumsum(); st=alld.groupby(run).agg(['min','max','size']).sort_values('size',ascending=False).head(1)

# ---------- on this day ----------
df['md']=df.ts.dt.strftime('%m-%d')
otd=df.groupby(['md','y','artist']).size().reset_index(name='plays').sort_values(['md','y','plays'],ascending=[True,True,False]).drop_duplicates(['md','y'])
tops=df.groupby(['md','y','artist','track']).size().reset_index(name='n').sort_values('n',ascending=False).drop_duplicates(['md','y','artist'])
otd=otd.merge(tops[['md','y','artist','track']],on=['md','y','artist'],how='left')
tot_=df.groupby(['md','y']).size().reset_index(name='day_total')
otd=otd.merge(tot_,on=['md','y']).rename(columns={'y':'year'})
save('on_this_day',otd)
# discovery year of current top 500
t5=R_now.head(500).index
dy=fe[t5].dt.year.value_counts().sort_index().reset_index(); dy.columns=['year','artists']
dy['examples']=[', '.join([a for a in t5 if fe[a].year==y][:4]) for y in dy.year]
save('discovery_top500',dy)
print('longest daily streak',st.to_dict('records'))
json.dump({'streak':{k:str(v) for k,v in st.iloc[0].items()},'app_snapshots':sum(1 for o in objs[1:] if o.get('data')),'app_first':objs[1]['timestamp'],'app_last':objs[-1]['timestamp']},open(f'{OUT}/extra.json','w'))
