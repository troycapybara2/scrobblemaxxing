import pandas as pd
df=pd.read_pickle('df.pkl'); df['y']=df.ts.dt.year
CORE="Attack Attack!|I See Stars|Asking Alexandria|Pierce the Veil|Sleeping With Sirens|Dance Gavin Dance|The Devil Wears Prada|Of Mice & Men|Underoath|Bring Me the Horizon|A Day to Remember|Alesana|Escape The Fate|A Skylit Drive|Issues|Abandon All Ships|I Set My Friends on Fire|Chiodos|From First to Last|Woe, Is Me|The Word Alive|Brokencyde|Knocked Loose|Gel|Dying Wish|Turnstile|La Dispute|Touché Amoré|Blessthefall|Crown the Empire|Motionless in White|Memphis May Fire|We Came as Romans|Attila|Counterparts|Every Time I Die|Pianos Become the Teeth|Sky Eats Airplane".split('|')
SOME="Hot Mulligan|Prince Daddy & The Hyena|Origami Angel|Title Fight|Sorority Noise|Microwave|Movements|Knuckle Puck|My Chemical Romance|Mayday Parade|Glocca Morra|Algernon Cadwallader|Balance and Composure|Basement|Bilmuri|Johnny Football Hero|Remo Drive|Sweet Pill|Tiny Moving Parts|PUP|Breathe Carolina".split('|')
tier=pd.Series({**{a:'Core screams' for a in CORE},**{a:'Some screams' for a in SOME}})
df['tier']=df.artist.map(tier)
rows=[]
for y,g in df.groupby('y'):
    c=g[g.tier=='Core screams']; s=g[g.tier=='Some screams']
    rows.append(dict(year=y,core_share=round(len(c)/len(g),4),some_share=round(len(s)/len(g),4),core_plays=len(c),some_plays=len(s),
        top_core=c.artist.value_counts().index[0] if len(c) else '',top_some=s.artist.value_counts().index[0] if len(s) else '',partial='yes' if y in (2011,2026) else 'no'))
Y=pd.DataFrame(rows); Y.to_csv('out/screams_year.csv',index=False)
a=df[df.tier.notna()].groupby(['tier','artist']).agg(plays=('uts','size')).reset_index()
pk=df[df.tier.notna()].groupby(['artist','y']).size().reset_index().sort_values(0).drop_duplicates('artist',keep='last').set_index('artist').y
a['peak_year']=a.artist.map(pk); a['plays_since_2023']=a.artist.map(df[df.y>=2023].artist.value_counts()).fillna(0).astype(int)
a=a.sort_values(['tier','plays'],ascending=[True,False]); a['rank']=a.groupby('tier').cumcount()+1
a.to_csv('out/screams_artists.csv',index=False)
print(Y[['year','core_share','some_share','top_core','top_some']].to_string())
print(a.groupby('tier').size().to_dict())
