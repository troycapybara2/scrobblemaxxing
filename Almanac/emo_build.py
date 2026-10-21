import pandas as pd, numpy as np, collections, itertools
df=pd.read_pickle('df.pkl'); df['y']=df.ts.dt.year
df['sess']=(df.uts.diff().fillna(1e9)>1800).cumsum(); df['mon']=df.ts.dt.strftime('%Y-%m')
W={
'2nd wave (90s Midwest)':"American Football|Mineral|The Get Up Kids|Cap'n Jazz|Braid|Christie Front Drive|Texas Is the Reason|Sunny Day Real Estate|Jimmy Eat World|The Promise Ring|Jawbreaker|Weezer|Penfold|Joan of Arc|Owls",
'3rd wave (2000s emo-pop)':"My Chemical Romance|Taking Back Sunday|Brand New|Say Anything|Dashboard Confessional|Saosin|The Used|Fall Out Boy|Panic! at the Disco|Paramore|The Starting Line|Motion City Soundtrack|Senses Fail|Thursday|Thrice|Mayday Parade|Silverstein|Hawthorne Heights|Cute Is What We Aim For|The Academy Is...|All Time Low|We The Kings|Sleeping With Sirens|Pierce the Veil|Escape The Fate|Breathe Carolina|Attack Attack!|I See Stars|Dance Gavin Dance|Asking Alexandria|The Devil Wears Prada|Of Mice & Men|A Day to Remember|Bring Me the Horizon|Never Shout Never|Boys Like Girls|Cobra Starship|Forever the Sickest Kids|The Ready Set|That's Outrageous!|Anarbor|You Me at Six|Falling in Reverse|Twenty One Pilots",
'4th wave (2010s revival)':"Title Fight|Modern Baseball|Tiny Moving Parts|The Hotelier|The World Is a Beautiful Place & I Am No Longer Afraid to Die|Tigers Jaw|Algernon Cadwallader|Turnover|Joyce Manor|Sorority Noise|Citizen|Basement|Pinegrove|Pity Sex|Dads|Into It. Over It.|Foxing|Marietta|Snowing|Glocca Morra|Balance and Composure|Microwave|Mat Kerekes|La Dispute|Touché Amoré|Pianos Become the Teeth|Hop Along|Remo Drive|Retirement Party|Kississippi|The Front Bottoms|Seahaven|Graduating Life|AJJ|Slaughter Beach, Dog|Kevin Devine",
'5th wave (post-emo)':"Mom Jeans.|Prince Daddy & The Hyena|Origami Angel|Hot Mulligan|macseal|oso oso|Super American|Your Arms Are My Cocoon|Weatherday|awakebutstillinbed|Sweet Pill|Jail Socks|saturdays at your place|Ogbert the Nerd|fanclubwallet|Equipment|Asian Glow|Glass Beach|The Brave Little Abacus|Lobsterfight|Another Michael|Insignificant Other|Fox Academy|Niiice.|Bay Faction|Thank You, I'm Sorry|They Are Gutting a Body of Water|hospital bracelet|Knope|Worst party ever|Local News Legend|Bilmuri|Johnny Football Hero|JANK|Blue Deputy|Riley!|cashcache!|armbite|Small Crush|Ovlov|pictures of vernon|Palette Knife|Retirement Party",
'Pop punk':"Real Friends|Neck Deep|The Story So Far|The Wonder Years|State Champs|Knuckle Puck|Man Overboard|Seaway|Four Year Strong|Movements|With Confidence|Moose Blood|Hit the Lights|Forever Came Calling|Major League|Transit|Broadway|Fireworks|Candy Hearts|Just Friends|blink-182|The Maine|Waterparks|PUP|We Are the In Crowd|With the Punches|This Wild Life|rationale.",
}
wave={}
for k,v in W.items():
    for a in v.split('|'): wave.setdefault(a,k)
FEEL={'Indie emo':"Turnover|oso oso|macseal|Super American|Pinegrove|Kississippi|Slaughter Beach, Dog|Equipment|Small Crush|Graduating Life|Retirement Party|Remo Drive|Knope|Blue Deputy|pictures of vernon",
 'Twinkle':"Algernon Cadwallader|Mom Jeans.|Prince Daddy & The Hyena|Origami Angel|Tiny Moving Parts|Snowing|Glocca Morra|Hot Mulligan|Sweet Pill|Johnny Football Hero|Ogbert the Nerd|Insignificant Other|Fox Academy|Niiice.|Bay Faction|macseal",
 'Pop-punk leaning':"Real Friends|Neck Deep|The Story So Far|The Wonder Years|State Champs|Knuckle Puck|Man Overboard|Seaway|Four Year Strong|With Confidence|Fireworks|Just Friends|Moose Blood|All Time Low|Mayday Parade|blink-182|Joyce Manor|Modern Baseball|The Front Bottoms|Microwave|Movements|rationale."}
feel={}
for k,v in FEEL.items():
    for a in v.split('|'): feel.setdefault(a,k)
sc=pd.read_csv('out/screams_artists.csv'); 
for t,a in zip(sc.tier,sc.artist):
    if t=='Core screams': feel[a]='Screamed'
    elif a not in feel: feel[a]='Some screams'
vc=df.artist.value_counts()
LANE=pd.read_csv('artist_lanes.csv').set_index('artist').lane
MAPLANES={'DIY emo','Emo revival 2.0','Indie emo','Emo revival 1.0','Warped Tour pop punk (2010s)'}
FALLBACK={'DIY emo':'5th wave (post-emo)','Emo revival 2.0':'5th wave (post-emo)','Indie emo':'4th wave (2010s revival)','Emo revival 1.0':'4th wave (2010s revival)','Warped Tour pop punk (2010s)':'Pop punk'}
EMO=[a for a in vc.index if LANE.get(a) in MAPLANES and vc[a]>=40]
for a in EMO: wave.setdefault(a,FALLBACK[LANE[a]])
for a in EMO:
    if LANE.get(a)=='Indie emo': feel[a]='Indie emo'
# time-adjusted co-listening lift among emo artists
S=df[df.artist.isin(EMO)].groupby('sess').agg(arts=('artist',lambda s:frozenset(s)),mon=('mon','first'))
occ=collections.Counter(); pair=collections.Counter(); mon_n=df.groupby('mon').sess.nunique(); mon_occ=collections.defaultdict(collections.Counter)
for arts,m in zip(S.arts,S.mon):
    for a in arts: occ[a]+=1; mon_occ[m][a]+=1
    for a,b in itertools.combinations(sorted(arts),2): pair[(a,b)]+=1
art_mon=collections.defaultdict(collections.Counter)
for m,c in mon_occ.items():
    for a,n in c.items(): art_mon[a][m]=n
def lift(b,a):
    c=pair.get((a,b) if a<b else (b,a),0); e=sum(n*mon_occ[m][a]/mon_n[m] for m,n in art_mon[b].items())
    return (c+1)/(e+1)
A={'pp':['State Champs','All Time Low','Four Year Strong','Fireworks','Seaway','With Confidence','We The Kings'],
   'emo':['American Football','Algernon Cadwallader','Mom Jeans.','Prince Daddy & The Hyena','Origami Angel','Tiny Moving Parts','Sweet Pill','Snowing'],
   'soft':['Turnover','oso oso','macseal','Super American','Pinegrove','Kississippi','Slaughter Beach, Dog'],
   'heavy':['Ogbert the Nerd','Prince Daddy & The Hyena','Riley!']}
HEAVY_SET={'Ogbert the Nerd':0.95,'Prince Daddy & The Hyena':0.82,'Riley!':0.8,'American Football':0.22}
A={k:[a for a in v if a in EMO] for k,v in A.items()}
def score(b,k): 
    xs=[np.log(lift(b,a)) for a in A[k] if a!=b]; return np.mean(xs) if xs else 0
rows=[]
for b in EMO:
    pp,em,so,he=score(b,'pp'),score(b,'emo'),score(b,'soft'),score(b,'heavy')
    cx=1/(1+np.exp(-(em-pp)*1.6)); cy=1/(1+np.exp(-(he-so)*1.6))
    f=feel.get(b,''); wv=wave[b]
    px={'Pop-punk leaning':0.28,'Indie emo':0.75,'Twinkle':0.82}.get(f,{'Pop punk':0.28,'3rd wave (2000s emo-pop)':0.35,'4th wave (2010s revival)':0.68,'5th wave (post-emo)':0.75,'2nd wave (90s Midwest)':0.8}[wv])
    py={'Screamed':0.8,'Some screams':0.6,'Pop-punk leaning':0.35,'Indie emo':0.1,'Twinkle':0.45}.get(f,0.4)
    x=0.5*px+0.5*cx; yv=0.7*py+0.3*cy
    if b in HEAVY_SET: yv=HEAVY_SET[b]
    rows.append(dict(artist=b,lane=LANE.get(b),wave=wave[b],feel=feel.get(b,''),plays=int(vc[b]),plays_since_2023=int((df[df.artist==b].y>=2023).sum()),
        peak_year=int(df[df.artist==b].y.value_counts().idxmax()),emo_score=round(x,3),heavy_score=round(yv,3)))
R=pd.DataFrame(rows).sort_values('plays',ascending=False)
# co-listening partners for tap highlighting (Jaccard on shared sessions, among bands shown on the map)
SHOWN={a for a in EMO if vc[a]>=60}
def partners(b,k=5):
    out=[]
    for a in SHOWN:
        if a==b: continue
        c=pair.get((a,b) if a<b else (b,a),0)
        if c>=3: out.append((c/(occ[a]+occ[b]-c),c,a))
    return '|'.join(f'{a}:{c}' for j,c,a in sorted(out,reverse=True)[:k])
R['partners']=R.artist.map(partners)
R.to_csv('out/emo_map.csv',index=False)
t=df[df.artist.isin(wave)].copy(); t['wave']=t.artist.map(wave)
Y=pd.crosstab(t.y,t.wave); tot=df.groupby('y').size()
out=[]
for y in Y.index:
    for w_ in W:
        out.append(dict(year=int(y),wave=w_,plays=int(Y.loc[y].get(w_,0)),share=round(Y.loc[y].get(w_,0)/tot[y],4),top_artist=(t[(t.y==y)&(t.wave==w_)].artist.value_counts().index[0] if Y.loc[y].get(w_,0) else '')))
pd.DataFrame(out).to_csv('out/emo_waves_year.csv',index=False)
print(R.head(40).to_string())
