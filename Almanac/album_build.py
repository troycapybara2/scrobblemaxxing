import pandas as pd, numpy as np, collections, random
df=pd.read_pickle('df.pkl')
df['sess']=(df.uts.diff().fillna(1e9)>1800).cumsum()
df['akey']=df.artist+' || '+df.album
df['single_rel']=(df.album.str.lower().str.strip()==df.track.str.lower().str.strip())|(df.album=='')
same=(df.akey==df.akey.shift())&(df.sess==df.sess.shift())&(df.album!='')
df['run']=(~same).cumsum()
df['y']=df.ts.dt.year
df.to_pickle('df_alb.pkl')
