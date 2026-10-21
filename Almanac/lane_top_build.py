import pandas as pd
df=pd.read_pickle('df.pkl'); df['y']=df.ts.dt.year
la=pd.read_csv('artist_lanes.csv').set_index('artist').lane
df['lane']=df.artist.map(la).fillna('Long tail')
rows=[]
for lane,g in df.groupby('lane'):
    for i,(a,n) in enumerate(g.artist.value_counts().head(15).items()):
        ga=g[g.artist==a]; yr=ga.y.value_counts()
        rows.append(dict(lane=lane,kind='artist',rank=i+1,name=a,artist=a,plays=int(n),peak_year=int(yr.idxmax())))
    tt=g.groupby(['artist','track']).size().sort_values(ascending=False).head(25)
    for i,((a,t),n) in enumerate(tt.items()):
        gt=g[(g.artist==a)&(g.track==t)]
        rows.append(dict(lane=lane,kind='track',rank=i+1,name=t,artist=a,plays=int(n),peak_year=int(gt.y.value_counts().idxmax())))
pd.DataFrame(rows).to_csv('out/lane_top.csv',index=False)
print(len(rows))
