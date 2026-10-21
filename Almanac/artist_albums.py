import pandas as pd
df=pd.read_pickle('df.pkl')
top=pd.read_csv('out/artist_profile.csv').artist.tolist()
g=df[(df.album!='')&df.artist.isin(top)].groupby(['artist','album']).agg(plays=('uts','size'),songs=('track','nunique'),first=('ts','min')).reset_index()
g=g[g.plays>=10].sort_values(['artist','plays'],ascending=[True,False])
g['rank']=g.groupby('artist').cumcount()+1
g=g[g['rank']<=10]; g['first']=g['first'].dt.strftime('%Y-%m-%d')
g[['artist','rank','album','plays','songs','first']].to_csv('out/artist_albums.csv',index=False)
