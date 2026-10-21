exec(open('life.py').read())
O='out/'
df['key']=df.artist+' — '+df.track
sc=pd.read_csv('artist_lanes.csv').set_index('artist').lane
df['scene']=df.artist.map(sc).fillna('Long tail')
NOW=df.ts.max()
rows=[]
for n,a,b,story in CH:
    g=df[df.chapter==n]; rest=df[df.chapter!=n]; end=min(T(b),NOW+pd.Timedelta(days=1)); days=(end-T(a)).days
    kc=g.groupby(['artist','track']).size().sort_values(ascending=False)
    rk=rest.groupby(['artist','track']).size()
    lift=(kc/len(g))/((rk.reindex(kc.index).fillna(0)+1)/len(rest))
    dfn=lift[kc>=15].sort_values(ascending=False).index[0]
    al=g[g.album!=''].groupby(['artist','album']).size().sort_values(ascending=False)
    rows.append(dict(chapter=n,start=a,end=(end-pd.Timedelta(days=1)).strftime('%Y-%m-%d'),story=story,days=days,scrobbles=len(g),per_day=round(len(g)/days,1),
      top_artist=g.artist.value_counts().index[0],top_artist_plays=int(g.artist.value_counts().iloc[0]),
      top_track=f"{kc.index[0][1]} ({kc.index[0][0]})",top_track_plays=int(kc.iloc[0]),top_album=f"{al.index[0][1]} ({al.index[0][0]})",
      defining_track=f"{dfn[1]} ({dfn[0]})",night_share=round(((g.h>=22)|(g.h<4)).mean(),3),weekend_share=round((g.dow>=5).mean(),3),
      top_scene=g[g.scene!='Long tail'].scene.value_counts().index[0]))
L=pd.DataFrame(rows); L.to_csv(O+'life_chapters.csv',index=False)
PER=[('Minute Media','2019-10-28','2025-09-20','NYC office, then remote through COVID and beyond'),('Villanova MBA','2023-01-18','2025-05-18','Grad school, alongside Minute Media'),('Elite','2025-10-06','2026-08-02','Working at Elite')]
prow=[]
for n,a,b_,story in PER:
    m=(df.ts>=T(a))&(df.ts<T(b_)); g=df[m]; rest=df[~m]; days=(min(T(b_),NOW+pd.Timedelta(days=1))-T(a)).days
    kc=g.groupby(['artist','track']).size().sort_values(ascending=False); rk=rest.groupby(['artist','track']).size()
    lift=(kc/len(g))/((rk.reindex(kc.index).fillna(0)+1)/len(rest)); dfn=lift[kc>=15].sort_values(ascending=False).index[0]
    al=g[g.album!=''].groupby(['artist','album']).size().sort_values(ascending=False)
    wd=g[g.dow<5]; work=wd[(wd.h>=9)&(wd.h<17)]
    prow.append(dict(period=n,start=a,end=(T(b_)-pd.Timedelta(days=1)).strftime('%Y-%m-%d'),story=story,days=days,scrobbles=len(g),per_day=round(len(g)/days,1),
      top_artist=g.artist.value_counts().index[0],top_artist_plays=int(g.artist.value_counts().iloc[0]),top_track=f"{kc.index[0][1]} ({kc.index[0][0]})",top_track_plays=int(kc.iloc[0]),
      top_album=f"{al.index[0][1]} ({al.index[0][0]})",defining_track=f"{dfn[1]} ({dfn[0]})",top_scene=g[g.scene!='Long tail'].scene.value_counts().index[0],
      workday_share=round(len(work)/len(g),3),workday_top_artist=work.artist.value_counts().index[0] if len(work) else ''))
pd.DataFrame(prow).to_csv(O+'life_periods.csv',index=False); print(pd.DataFrame(prow).T.to_string()); print(L[['chapter','end','per_day','top_track','defining_track']].to_string())
mk=sorted([('2015-08-31','Start of college'),('2019-10-28','First day at Minute Media (NYC office)'),('2020-03-16','COVID lockdown'),('2020-09-01','Move to Bloomfield, NJ'),('2021-09-01','Move to Philly'),('2023-01-18','Started the Villanova MBA'),('2024-09-01','Move to Bristol with Katie'),('2024-11-01','Engaged'),('2025-05-17','MBA graduation'),('2025-09-19','Last day at Minute Media'),('2025-10-06','Started at Elite'),('2026-08-01','Last day at Elite'),('2026-08-09','Wedding')])
mr=[]
for d,l in mk:
    s=T(d); g=df[(df.ts>=s)&(df.ts<s+pd.Timedelta(days=30))]; kc=g.groupby(['artist','track']).size().sort_values(ascending=False)
    mr.append(dict(date=d,event=l,top_song_next_30_days=f"{kc.index[0][1]} ({kc.index[0][0]})",plays=int(kc.iloc[0])))
pd.DataFrame(mr).to_csv(O+'life_markers.csv',index=False)
hs=df[(df.chapter=='High school')&(df.dow<5)&(~df.m.isin([7,8]))]
col=df[(df.chapter=='College')&(~df.m.isin([6,7,8]))]
cf=col[col.dow.isin([4,5])]; co=col[~col.dow.isin([4,5])]
rh=[]
for name,g in [('High school weekdays',hs),('College Fri and Sat',cf),('College other days',co)]:
    nd=g.d.nunique(); c=g.groupby('h').size()
    for h in range(24): rh.append(dict(routine=name,hour=h,plays_per_day=round(c.get(h,0)/nd,2)))
pd.DataFrame(rh).to_csv(O+'routine_hours.csv',index=False)
rs=[]
bus=hs[hs.h.isin([14,15])]; pre=col[col.dow.isin([4,5])&col.h.between(20,22)]
for name,g,base,minp in [('Bus ride',bus,hs,8),('Pregame',pre,col,6)]:
    kc=g.groupby(['artist','track']).size(); bc=base.groupby(['artist','track']).size()
    lift=(kc/len(g))/(bc.reindex(kc.index)/len(base))
    top=lift[kc>=minp].sort_values(ascending=False).head(12)
    for i,((a,t),v) in enumerate(top.items()): rs.append(dict(routine=name,rank=i+1,artist=a,track=t,plays=int(kc[(a,t)]),times_more_likely=round(v,1)))
pd.DataFrame(rs).to_csv(O+'routine_songs.csv',index=False)
MN=['January','February','March','April','May','June','July','August','September','October','November','December']
t=df.groupby(['artist','track','m']).agg(n=('uts','size'),years=('y','nunique')).reset_index()
tot=df.groupby(['artist','track']).size().rename('total')
t=t.join(tot,on=['artist','track']); t['lift']=(t.n/t.total*12).round(1)
rows=[]
for m in range(1,13):
    x=t[(t.m==m)&(t.years>=3)&(t.lift>=1.5)].sort_values(['years','lift','n'],ascending=False).head(6)
    for i,r in enumerate(x.itertuples()):
        rows.append(dict(month=MN[m-1],month_num=m,rank=i+1,artist=r.artist,track=r.track,years_returned=int(r.years),plays_in_month=int(r.n),total_plays=int(r.total),times_usual_rate=r.lift))
MS=pd.DataFrame(rows); MS.to_csv(O+'month_songs.csv',index=False); print(MS[MS['rank']==1][['month','artist','track','years_returned','times_usual_rate']].to_string())
full=df[(df.y>=2012)&(df.y<=2025)]
ys=full.groupby(['y','scene']).size()/full.groupby('y').size()
ms=full.groupby(['y','m','scene']).size()/full.groupby(['y','m']).size()
r=(ms/ys.reindex(ms.index.droplevel(1)).values).rename('ratio').reset_index()
r=r[r.apply(lambda q: ys.get((q.y,q.scene),0)>=0.02,axis=1)]
big=full[full.scene!='Long tail'].scene.value_counts(); big=set(big[big>=1500].index)
r=r[r.scene.isin(big)]
S=r.groupby(['m','scene']).ratio.mean().round(2).reset_index()
S['month']=S.m.map(lambda m:MN[m-1]); S=S.rename(columns={'m':'month_num','ratio':'seasonal_index'})
S[['month','month_num','scene','seasonal_index']].to_csv(O+'month_scenes.csv',index=False)
pv=S.pivot(index='month_num',columns='scene',values='seasonal_index')
print(pv.round(2).T.to_string())
rh=pd.DataFrame(rh); print(rh[rh.routine=='High school weekdays'].set_index('hour').plays_per_day.loc[[13,14,16]].to_dict())
