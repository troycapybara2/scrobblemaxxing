import pandas as pd, json
exec(open('albumnorm.py').read())
df=pd.read_pickle('df_raw.pkl')
df['album_raw']=df.album
al=df[df.album!=''].groupby(['artist','album']).size().reset_index(name='n')
al['b']=al.album.map(base); al['bl']=al.b.str.lower()
disp=al.sort_values('n',ascending=False).drop_duplicates(['artist','bl']).set_index(['artist','bl']).b
al['display']=[disp[(a,b)] for a,b in zip(al.artist,al.bl)]
m={(a,x):d for a,x,d in zip(al.artist,al.album,al.display)}
df['album']=[m.get((a,x),x) if x else x for a,x in zip(df.artist,df.album)]
df.to_pickle('df.pkl')
# album art: add rows under merged display names
P='/tmp/art3.json'; art=json.load(open(P)); rows=[]; have=set()
# covers Capy sent himself (my_covers.json, same 'Artist || Album' keys) win over the downloaded ones
import os
if os.path.exists('my_covers.json'): art.update(json.load(open('my_covers.json')))
for k,v in art.items():
    if not v: continue
    a,x=k.split(' || ',1); d=disp.get((a,base(x).lower()), base(x))
    for name in [x,d]:
        if (a.lower(),name.lower()) not in have: rows.append({'artist':a,'album':name,'img':v}); have.add((a.lower(),name.lower()))
json.dump(rows,open('art_merged.json','w'),ensure_ascii=False)
print('albums before',df.album_raw.nunique(),'after',df.album.nunique(),'art rows',len(rows))
