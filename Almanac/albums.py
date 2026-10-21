import pandas as pd, numpy as np, collections, random
df=pd.read_pickle('df_alb.pkl')
# run = consecutive plays of same album within a session (repeats allowed but counted by distinct)
rd=df.groupby('run').track.nunique(); df['run_distinct']=df.run.map(rd)
df['in_album_run']=(df.run_distinct>=3)&(df.album!='')
yr=df.groupby('y').agg(plays=('uts','size'),album_runs=('in_album_run','mean'),single_rel=('single_rel','mean')).reset_index()
A=df[(df.album!='')&(~df.single_rel)]
cnt=A.akey.value_counts(); keys=cnt[cnt>=40].index
print('albums >=40',len(keys))
def order_stats(runs):
    # runs: list of lists of tracks (distinct-consecutive sequences, len>=3), dedup consecutive repeats
    nxt=collections.defaultdict(collections.Counter)
    for r in runs:
        for a,b in zip(r,r[1:]):
            if a!=b: nxt[a][b]+=1
    succ={a:c.most_common(1)[0][0] for a,c in nxt.items()}
    tot=hit=0
    for r in runs:
        for a,b in zip(r,r[1:]):
            if a==b: continue
            tot+=1; hit+= succ.get(a)==b
    return (hit/tot if tot else np.nan), tot, succ, nxt
rows=[]; rng=random.Random(7); orders={}
for k in keys:
    g=A[A.akey==k]
    s=g.groupby('sess').track.nunique()
    tc=g.track.value_counts()
    runs=[]
    for rid,rg in g.groupby('run'):
        seq=[t for i,t in enumerate(rg.track) if i==0 or t!=rg.track.iloc[i-1]]
        if len(seq)>=3: runs.append(seq)
    io,tot,succ,nxt=order_stats(runs)
    # null: shuffle each run
    nulls=[]
    for _ in range(20):
        sh=[rng.sample(r,len(r)) for r in runs]
        nulls.append(order_stats(sh)[0])
    rows.append(dict(artist=g.artist.iloc[0],album=g.album.iloc[0],plays=len(g),songs=g.track.nunique(),
        top_track=tc.index[0],top_track_share=round(tc.iloc[0]/len(g),3),top2_share=round(tc.iloc[:2].sum()/len(g),3),
        sessions=len(s),single_song_sessions=round((s==1).mean(),3),album_sessions=round((s>=4).mean(),3),
        plays_in_album_runs=round(g.in_album_run.mean(),3),transitions=tot,in_order=round(io,3) if tot else None,
        shuffle_baseline=round(float(np.nanmean(nulls)),3) if tot else None,
        first=g.ts.min().strftime('%Y-%m-%d')))
    orders[k]=(succ,nxt,runs)
R=pd.DataFrame(rows)
import pickle; pickle.dump(orders,open('orders.pkl','wb'))
R.to_pickle('albums_metrics.pkl'); yr.to_pickle('alb_year.pkl')
