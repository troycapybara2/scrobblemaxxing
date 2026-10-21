import pandas as pd, numpy as np, collections, itertools, networkx as nx
exec(open('affinity.py').read())   # df (with sess, mon), vc, TOP, occ, pair, mon_occ, art_mon, shared(), expected()
O='out/'
NOW=df.ts.max(); df['y']=df.ts.dt.year; df['h']=df.ts.dt.hour
fe=df.groupby('artist').ts.min()
# volume-adjusted rank
mt=df.groupby('mon').size(); wgt=df.mon.map(mt.mean()/mt)
sw=wgt.groupby(df.artist).sum().sort_values(ascending=False)
adj_rank=pd.Series(np.arange(1,len(sw)+1),index=sw.index)
age=((NOW-fe).dt.days/365.25)
ppy=(vc/age.clip(lower=1)).round(1)
# burn speed
def half(t):
    t=t.sort_values().reset_index(drop=True); return (t.iloc[len(t)//2]-t.iloc[0]).days
big=vc[vc>=100].index
hl=df[df.artist.isin(big)].groupby('artist').ts.apply(half)
def burn(d):
    return 'Flash' if d<=180 else ('Fast' if d<=730 else ('Steady' if d<=2190 else 'Slow burn'))
# opener rate
first=df.groupby('sess').artist.first().value_counts(); insess=df.groupby('artist').sess.nunique()
opener=(first.reindex(insess.index).fillna(0)/insess)
# night lift vs that year's baseline
df['night']=(df.h>=22)|(df.h<4); yb=df.groupby('y').night.mean(); df['exp']=df.y.map(yb)
nl=df.groupby('artist').agg(obs=('night','sum'),exp=('exp','sum'),n=('night','size')); nlift=(nl.obs/nl.exp)
# augment artist_profile
ap=pd.read_csv(O+'artist_profile.csv')
ap['adj_rank']=ap.artist.map(adj_rank).astype(int)
ap['plays_per_year']=ap.artist.map(ppy)
ap['half_life_days']=ap.artist.map(hl).astype('Int64'); ap['burn']=ap.half_life_days.map(lambda d: burn(d) if pd.notna(d) else '')
ap['opener_rate']=ap.artist.map(opener).round(3)
ap['night_lift']=ap.artist.map(nlift).round(2)
ap.to_csv(O+'artist_profile.csv',index=False)
t5=pd.read_csv(O+'top500_now.csv',dtype=str,keep_default_na=False)
t5['adj_rank']=t5.artist.map(adj_rank).astype(int); t5['adj_moved']=t5.rank_now.astype(int)-t5.adj_rank
t5['plays_per_year']=t5.artist.map(ppy)
t5.to_csv(O+'top500_now.csv',index=False)
# most connected (time-adjusted lift)
rows=[]
for b in ap.artist:
    if b not in T: continue
    cands=[]
    for a in TOP:
        if a==b: continue
        c=shared(a,b)
        if c<8: continue
        e=expected(b,a); cands.append((round((c+1)/(e+1),2),c,round(e,1),a))
    for lift,c,e,a in sorted(cands,reverse=True)[:6]:
        rows.append(dict(artist=b,neighbor=a,shared_sessions=c,expected_sessions=e,lift=lift))
pd.DataFrame(rows).to_csv(O+'artist_connected.csv',index=False)
# exploration share per year
df['new90']=(df.ts-df.artist.map(fe)).dt.days<=90
yr=pd.read_csv(O+'yearly.csv'); yr['exploration_share']=yr.year.map(df.groupby('y').new90.mean().round(3)); yr.to_csv(O+'yearly.csv',index=False)
# time-of-day fingerprint
g=nl[nl.n>=300].copy(); g['night_lift']=(g.obs/g.exp).round(2)
nt=g.sort_values('night_lift',ascending=False).head(8).assign(kind='Night'); dy=g.sort_values('night_lift').head(8).assign(kind='Day')
tf=pd.concat([nt,dy]).reset_index().rename(columns={'index':'artist','n':'plays'})[['artist','kind','plays','night_lift']]
tf.to_csv(O+'time_fingerprint.csv',index=False)
# heating up
l30=df[df.ts>NOW-pd.Timedelta(days=30)].artist.value_counts()
p365=df[(df.ts<=NOW-pd.Timedelta(days=30))&(df.ts>NOW-pd.Timedelta(days=395))].artist.value_counts()
hu=pd.DataFrame({'plays_30d':l30,'plays_prior_year':p365.reindex(l30.index).fillna(0).astype(int)})
hu=hu[hu.plays_30d>=12]
hu['pace_vs_normal']=((hu.plays_30d/30)/((hu.plays_prior_year+3)/365)).round(1)
hu=hu.sort_values('pace_vs_normal',ascending=False).head(10).reset_index().rename(columns={'index':'artist'})
na=pd.read_csv(O+'now_artists.csv').set_index('artist').bucket
hu['bucket']=hu.artist.map(na).fillna('Everything else'); hu['rank']=range(1,len(hu)+1)
hu.to_csv(O+'heating_up.csv',index=False)
# discovery class retention
d=df[['artist','ts']].copy(); d['age']=(d.ts-d.artist.map(fe)).dt.days
y1=d[d.age<365].groupby('artist').size(); coh=y1[y1>=30].index
y3=d[(d.age>=730)&(d.age<1095)].groupby('artist').size()
r=pd.DataFrame({'year':fe[coh].dt.year,'kept':(y3.reindex(coh).fillna(0)>=10)})
r=r[r.year<=2023].groupby('year').kept.agg(['mean','size']).reset_index()
r.columns=['year','kept_share','artists_hooked']; r['kept_share']=r.kept_share.round(3)
ex=[]
for y in r.year:
    ks=[a for a in coh if fe[a].year==y and y3.get(a,0)>=10]
    ex.append(', '.join(sorted(ks,key=lambda a:-vc[a])[:3]))
r['still_playing']=ex
r.to_csv(O+'discovery_retention.csv',index=False)
print(ap[['artist','adj_rank','plays_per_year','half_life_days','burn','opener_rate','night_lift']].head(8).to_string())
print(hu.to_string()); print(r.to_string())
