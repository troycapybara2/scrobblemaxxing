import pandas as pd, numpy as np, re, os, collections
exec(open('buckets6.py').read())
exec(open('playlist.py').read())
O='out/'
U='Underground & rap'
FAM={'Michigan':U,'Underground':U,'SoundCloud':U,'Mainstream':U,'Alt rap':U,'West coast':U,'Female rap':U,'Hyperpop':U,
'Pop':'Pop, R&B & country','R&B':'Pop, R&B & country','Country & folk':'Pop, R&B & country',
'Emo revival 2.0':'Emo & indie','DIY emo':'Emo & indie','EDM':'EDM','Indie emo':'Emo & indie','Indie':'Emo & indie','Emo revival 1.0':'Emo & indie','Warped Tour pop punk (2010s)':'Emo & indie','Scene kid (2000s)':'Emo & indie',
'Old rock appreciation':'Classics','Appreciating the greats':'Classics','Old rap':'Classics','Folk punk':'Emo & indie','Blog-era nostalgia':'Classics','Grab bag':'Other','Everything else':'Other'}
ORDER=list(FAM)
E['y']=E.ts.dt.year; E['we']=E.ts.dt.dayofweek>=5
E['q']=E.ts.dt.year.astype(str)+'-Q'+E.ts.dt.quarter.astype(str)
Q=E[E.q!='2026-Q4']
qt=Q.groupby(['q','bucket']).size().unstack(fill_value=0).reindex(columns=ORDER,fill_value=0)
qs=qt.div(qt.sum(axis=1),axis=0)
pd.DataFrame([dict(quarter=q,bucket=b,plays=int(qt.loc[q,b]),share=round(qs.loc[q,b],4)) for q in qt.index for b in ORDER]).to_csv(O+'now_quarterly.csv',index=False)
ys=pd.crosstab(E.bucket,E.y,normalize='columns')
br=[]
for b in ORDER:
    g=E[E.bucket==b]; g6=g[g.y==2026]
    tt=g.groupby(['artist','track']).size().sort_values(ascending=False); pk=qs[b].idxmax()
    br.append(dict(bucket=b,family=FAM[b],plays=len(g),share_era=round(len(g)/len(E),4),plays_2023=int((g.y==2023).sum()),plays_2024=int((g.y==2024).sum()),plays_2025=int((g.y==2025).sum()),plays_2026=int((g.y==2026).sum()),share_2023=round(ys.loc[b,2023],4),share_2024=round(ys.loc[b,2024],4),share_2025=round(ys.loc[b,2025],4),share_2026=round(ys.loc[b,2026],4),
      change_pts=round((ys.loc[b,2026]-ys.loc[b,2023])*100,1),artists=g.artist.nunique(),
      leads_2026=', '.join((g6 if len(g6) else g).artist.value_counts().index[:4]),signature_track=f"{tt.index[0][1]} ({tt.index[0][0]})",signature_plays=int(tt.iloc[0]),
      peak_quarter=pk,peak_share=round(qs.loc[pk,b],4),weekend_share=round(g.we.mean(),3),
      sublanes=' · '.join(f"{k}: {', '.join(g[g.artist.map(sub)==k].artist.value_counts().index[:5])} ({round((g.artist.map(sub)==k).mean()*100)}% of plays)" for k in dict.fromkeys(x for x in g.artist.map(sub).dropna()))))
bd=pd.DataFrame(br); bd.to_csv(O+'now_buckets.csv',index=False)
tops=[]
for b in ORDER:
    g=E[E.bucket==b]
    for i,(a,n) in enumerate(g.artist.value_counts().head(20).items()):
        tops.append(dict(bucket=b,kind='artist',rank=i+1,name=a,artist=a,plays=int(n),plays_2026=int(((g.artist==a)&(g.y==2026)).sum())))
    tt=g.groupby(['artist','track']).size().sort_values(ascending=False).head(12)
    for i,((a,t),n) in enumerate(tt.items()):
        tops.append(dict(bucket=b,kind='track',rank=i+1,name=t,artist=a,plays=int(n),plays_2026=int(((g.artist==a)&(g.track==t)&(g.y==2026)).sum())))
pd.DataFrame(tops).to_csv(O+'bucket_top.csv',index=False)
print(bd[['bucket','plays','share_2023','share_2026','weekend_share','leads_2026','sublanes']].to_string())
fe=df.groupby('artist').ts.min()
ar=E.groupby('artist').agg(plays_since_2023=('uts','size'),bucket=('bucket','first')).join(E[E.y==2026].artist.value_counts().rename('plays_2026')).fillna({'plays_2026':0})
ar=ar[ar.plays_since_2023>=15].sort_values('plays_since_2023',ascending=False).reset_index()
ar['plays_2026']=ar.plays_2026.astype(int); ar['first_heard']=ar.artist.map(fe).dt.strftime('%Y-%m-%d')
ar['sublane']=ar.artist.map(sub).fillna('')
ar['how_tagged']=ar.artist.map(lambda a:'you / seed list' if a in seed else ('co-listening' if a in prop else 'untagged'))
ar[['artist','bucket','sublane','plays_since_2023','plays_2026','first_heard','how_tagged']].to_csv(O+'now_artists.csv',index=False)
# playlist + drives
n=lambda s: re.sub(r'[^a-z0-9]','',re.sub(r'^the ','',str(s).lower()))
d2=df.copy(); d2['an']=d2.artist.map(n); d2['tn']=d2.track.map(lambda s: re.sub(r'[^a-z0-9]','',str(s).lower()))
amap={n(k):v for k,v in assign.items()}
pl=[]; hit=pd.Series(False,index=d2.index)
for a,t in PL:
    an=n(a); tn=re.sub(r'[^a-z0-9]','',t.lower())
    m=d2.an.str.contains(an[:10],regex=False)&d2.tn.str.startswith(tn[:12]); hit|=m
    pl.append(dict(artist=a,track=t,bucket=amap.get(an,'Everything else'),scrobbles=int(m.sum()),first_scrobble=d2[m].ts.min().strftime('%Y-%m-%d') if m.any() else ''))
pd.DataFrame(pl).to_csv(O+'now_playlist.csv',index=False)
d2['pl']=hit
EE=d2[d2.ts>=pd.Timestamp('2023-01-01',tz='America/New_York')]
s=EE.groupby('sess').agg(n=('uts','size'),pl=('pl','sum'),start=('ts','min'),end=('ts','max'))
D=s[(s.pl>=4)&(s.pl/s.n>=.5)]
dr=[]
for sid,r in D.iterrows():
    g=EE[EE.sess==sid]
    dr.append(dict(date=r.start.strftime('%Y-%m-%d'),day=r.start.strftime('%A'),start=r.start.strftime('%-I:%M %p'),minutes=int(round((r.end-r.start).total_seconds()/60))+3,scrobbles=int(r.n),playlist_songs=int(r.pl),most_played=g.artist.value_counts().index[0]))
pd.DataFrame(dr).to_csv(O+'now_drives.csv',index=False); print(pd.DataFrame(dr))

# ---- With the trop overlay (cross-genre) ----
pls={(re.sub(r'[^a-z0-9]','',re.sub(r'^the ','',a.lower()))[:10], re.sub(r'[^a-z0-9]','',t.lower())[:12]) for a,t in PL}
def on_pl(a,t):
    an=re.sub(r'[^a-z0-9]','',re.sub(r'^the ','',str(a).lower())); tn=re.sub(r'[^a-z0-9]','',str(t).lower())
    return any(x in an and tn.startswith(y) for x,y in pls)
pair_pl={k:on_pl(*k) for k in E.groupby(['artist','track']).size().index}
E['trop']=E.artist.isin(TROP).values|np.array([pair_pl[(a,t)] for a,t in zip(E.artist,E.track)])
ty=E.groupby('y').agg(plays=('trop','sum'),total=('trop','size')).reset_index().rename(columns={'y':'year'})
ty['share']=(ty.plays/ty.total).round(4); ty['plays']=ty.plays.astype(int)
ty['weekend_share']=ty.year.map(E[E.trop].groupby('y').we.mean().round(3))
ty[['year','plays','share','weekend_share']].to_csv(O+'trop_year.csv',index=False)
T=E[E.trop]
mx=T.bucket.value_counts().reset_index(); mx.columns=['bucket','plays']; mx['share_of_trop']=(mx.plays/len(T)).round(3); mx=mx[mx.plays>=10]
mx.to_csv(O+'trop_mix.csv',index=False)
ta=T.artist.value_counts().head(15).reset_index(); ta.columns=['artist','plays']; ta['rank']=range(1,len(ta)+1); ta['bucket']=ta.artist.map(assign).fillna('Everything else')
ta['plays_2026']=ta.artist.map(T[T.y==2026].artist.value_counts()).fillna(0).astype(int)
ta.to_csv(O+'trop_artists.csv',index=False)
print(ty.to_string()); print(mx.head(10).to_string()); print('trop weekend', round(T.we.mean(),3), 'all', round(E.we.mean(),3))
