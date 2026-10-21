import pickle, collections, numpy as np, pandas as pd, random
orders=pickle.load(open('orders.pkl','rb'))
R=pd.read_pickle('albums_metrics.pkl')
def loo(runs):
    nxt=collections.defaultdict(collections.Counter)
    for r in runs:
        for a,b in zip(r,r[1:]):
            if a!=b: nxt[a][b]+=1
    tot=hit=0
    for r in runs:
        own=collections.Counter((a,b) for a,b in zip(r,r[1:]) if a!=b)
        for a,b in zip(r,r[1:]):
            if a==b: continue
            c=collections.Counter(nxt[a])
            for (x,y),n in own.items():
                if x==a: c[y]-=n
            c={k:v for k,v in c.items() if v>0}
            if not c: continue
            tot+=1; m=max(c.values()); best=[k for k,v in c.items() if v==m]
            hit+=(b in best)/len(best)
    return hit/tot if tot else np.nan, tot
rng=random.Random(3); res=[]
for k,(succ,nxt,runs) in orders.items():
    io,tot=loo(runs); nl=[loo([rng.sample(r,len(r)) for r in runs])[0] for _ in range(10)]
    res.append((k,io,tot,np.nanmean(nl) if tot else np.nan))
L=pd.DataFrame(res,columns=['akey','loo','loo_n','loo_null'])
R['akey']=R.artist+' || '+R.album; R=R.merge(L,on='akey')
R=R[(R.songs>=3)&~R.album.str.contains(r' - Single$',regex=True)].copy()
R['in_order']=np.where(R.loo_n>=20,R.loo.round(3),np.nan)
R['shuffle_baseline']=np.where(R.loo_n>=20,R.loo_null.round(3),np.nan)
def st(r):
    if r.top_track_share>=0.5: return 'One-song album'
    if r.plays_in_album_runs>=0.5:
        if not np.isnan(r.in_order) and r.in_order<0.35: return 'Album, shuffled'
        return 'Front to back'
    if r.plays_in_album_runs<0.25: return 'Playlist picks'
    return 'Mixed'
R['listen_style']=R.apply(st,axis=1)
sc=pd.read_csv('artist_lanes.csv').rename(columns={'lane':'scene'})[['artist','scene']]
R=R.merge(sc,on='artist',how='left'); R['scene']=R.scene.fillna('Long tail')
cols=['artist','album','plays','songs','top_track','top_track_share','single_song_sessions','plays_in_album_runs','in_order','shuffle_baseline','listen_style','scene','first']
R.sort_values('plays',ascending=False)[cols].to_csv('out/album_styles.csv',index=False)
df=pd.read_pickle('df_alb.pkl')
rd=df.groupby('run').track.nunique(); df['in_album_run']=(df.run.map(rd)>=3)&(df.album!='')
df['single_rel']=(df.album.str.lower().str.strip()==df.track.str.lower().str.strip())|df.album.str.contains(r' - Single$',regex=True)
Y=df.groupby('y').agg(plays=('uts','size'),album_run_plays=('in_album_run','sum'),single_release_plays=('single_rel','sum')).reset_index().rename(columns={'y':'year'})
Y['album_run_share']=(Y.album_run_plays/Y.plays).round(3); Y['single_release_share']=(Y.single_release_plays/Y.plays).round(3)
Y.to_csv('out/album_year.csv',index=False)
