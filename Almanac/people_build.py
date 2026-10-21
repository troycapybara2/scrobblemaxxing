import pandas as pd
df=pd.read_pickle('df.pkl')
P=[('Katie','Your wife. Her favorites that made it into your rotation, plus the three songs from your wedding on Aug 9, 2026.',[('Pinegrove',None),('oso oso',None),('Waxahatchee','Right Back to It'),('Lil Uzi Vert','Paradise'),('Mayday Parade','Piece Of Your Heart')]),
('Ian','Put you on in college in Poughkeepsie, then roommates in Bloomfield, NJ.',[('Mom Jeans.',None),('Perspective, a lovely hand to hold',None),('Quinn Cicala','In a Diner in Poughkeepsie'),('Calvin Harris','Slide')]),
('Jeff','Lived together for a minute in Philly.',[('Tigers Jaw','Plane vs. Tank vs. Submarine'),('American Football','Never Meant'),('Sammy Adams','All Night Longer'),('Young Money','BedRock')]),
('B-Lit','Lived together in Philly.',[('Playboi Carti','wokeuplikethis'),('Pi’erre Bourne',None),('Lil Yachty','Poland')]),
('Chris','Friend. Both go back to your first weeks on Last.fm.',[('My Chemical Romance',None),('Breathe Carolina',None)])]
rows=[]
for order,(person,ctx,items) in enumerate(P):
    for i,(a,t) in enumerate(items):
        g=df[df.artist==a]
        if t: g=g[g.track.str.lower().str.startswith(t.lower())]
        alb=g[g.album!=''].album.value_counts()
        rows.append(dict(person=person,person_order=order+1,context=ctx,item_order=i+1,kind='song' if t else 'artist',artist=a,track=(g.track.value_counts().index[0] if t else ''),
          label=(g.track.value_counts().index[0] if t else a),plays=len(g),first_heard=g.ts.min().strftime('%Y-%m-%d'),last_heard=g.ts.max().strftime('%Y-%m-%d'),
          plays_2026=int((g.ts.dt.year==2026).sum()),peak_year=int(g.ts.dt.year.value_counts().idxmax()),album=alb.index[0] if len(alb) else ''))
pd.DataFrame(rows).to_csv('out/people_links.csv',index=False)
print(pd.DataFrame(rows)[['person','label','plays','first_heard']].head(6))
