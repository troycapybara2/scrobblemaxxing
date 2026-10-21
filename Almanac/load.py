import json,pandas as pd
def load_lb():
    s=open('leaderboard_history.json').read()
    dec=json.JSONDecoder();i=0;objs=[]
    while i<len(s):
        while i<len(s) and s[i] in ' \n\r\t': i+=1
        if i>=len(s): break
        o,j=dec.raw_decode(s,i); objs.append(o); i=j
    return objs
def load_df():
    df=pd.read_csv('/mnt/user-data/uploads/recenttracks-troycapybara-1791891883.csv')
    df=df[df.uts>1e9].copy()
    df['dt']=pd.to_datetime(df.uts,unit='s',utc=True).dt.tz_convert('America/New_York')
    return df.sort_values('uts').reset_index(drop=True)
import re,collections
def norm(a): return re.sub(r'[^a-z0-9]','',str(a).lower().replace('$','s'))
def clean_df():
    df=load_df()
    c=df.artist.value_counts()
    groups=collections.defaultdict(dict)
    for a,v in c.items(): groups[norm(a)][a]=int(v)
    amap={}
    for k,v in groups.items():
        if len(v)>1 and k not in ('','key'):
            canon=max(v,key=v.get)
            for a in v: amap[a]=canon
    amap['Travi$ Scott']='Travis Scott'; amap['Travis Scott']='Travis Scott'
    df['artist']=df.artist.map(lambda a: amap.get(a,a))
    df['album']=df.album.fillna('')
    return df
