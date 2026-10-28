from collections import Counter
import pandas as pd, re, json, unicodedata
exec(open('picks.py').read().replace('print(len(PICKS))',''))
fix={
 "Charmer":"Loud, sad, and fun emo revival 2.0. Built for the Hot Mulligan crowd.",
 "Ben Quad":"Riffy emo with big gang vocals. Sits right with Hot Mulligan.",
 "Acid Rap":"The Chicago mixtape that made Chance. A must-own for the library.",
 "Untrue":"Rainy-night London garage. Hugely loved by the Drain Gang crowd.",
 "Melodrama":"A critics' favorite of the 2010s, and Lorde at her best.",
 "The Miseducation of Lauryn Hill":"Rap and soul at once. Modern R&B leans on it constantly.",
 "To Pimp a Butterfly":"Jazz, funk and Thundercat basslines. Sits at the top of RYM's all-time chart.",
 "Madvillainy":"A fixture of RYM's all-time top 10. Earl's whole sound points back to it.",
 "Nightmare Vacation":"Punk-rap with 100 gecs' Dylan Brady on production.",
 "Proper":"Evan Weiss at his most hook-forward.",
 "Crooked Rain, Crooked Rain":"Slacker rock with great melodies. The friendliest Pavement record.",
 "Asleep in the Bread Aisle":"Frat-rap origin story. Asher Roth grew up in Morrisville, PA.",
}
exec(open('rym.py').read())
exec(open('rym2.py').read())
for r in RYM:
    if r['rank']==153: r['album']='Jenny Death'; r['alts']='thepowersthatb,jennydeath'
def kn(a,b):
    import re as _r
    f=lambda x:_r.sub(r'[^a-z0-9]','',x.lower().replace('&','and'))
    return f(a)+'|'+f(_r.sub(r'\(.*?\)','',b))
idx={kn(p['artist'],p['album']):p for p in PICKS}
for r in RYM:
    k=kn(r['artist'],r['album'])
    if k in idx: idx[k]['rymRank']=r['rank']; idx[k]['rymRating']=r['rating']; continue
    if not r['lane']: print('NO MATCH, NO DATA',r['rank'],r['album']); continue
    p=dict(artist=r['artist'],album=r['album'],year=int(r['year']) if r['year'] else None,lane=r['lane'],canon=r['canon'],anchors=[x for x in r['anchors'].split(';') if x],why=r['why'],home='',rymRank=r['rank'],rymRating=r['rating'])
    if r['alts']: p['alts']=r['alts']
    PICKS.append(p); idx[k]=p
for p in PICKS:
    if p['album'] in fix: p['why']=fix[p['album']]
    if p['artist']=='Charmer' or p['artist']=='Ben Quad': p['why']=fix[p['artist']]

df=pd.read_csv('/home/claude/scrobblemaxxing/data/scrobbles.csv'); df=df[df.uts>1e9].copy()
df['album']=df.album.fillna('')
def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
    s=s.replace('&','and').replace('’',"'")
    s=re.sub(r'\(.*?\)|\[.*?\]','',s)
    s=re.sub(r'\b(deluxe|remaster(ed)?|edition|expanded|anniversary|version)\b.*','',s)
    return re.sub(r'[^a-z0-9]','',s)
df['an']=df.artist.map(norm); df['bn']=df.album.map(norm)
alias={'thestooges':['iggyandthestooges','iggypop'],'neilyoung':['neilyoungandcrazyhorse','neilyoungcrazyhorse'],'gza':['geniusgza','gzagenius','genius'],'brianeno':['eno'],'janetjackson':['janet'],'dinosaurjr':['dinosaur'],'three6mafia':['threesixmafia','three6mafia'],'prince':['princeandtherevolution'],'paulmccartney':['paulandlindamccartney','paulmccartneylindamccartney'],'jpegmafiaanddannybrown':['jpegmafia','dannybrown'],'felakuti':['felakutiandtheafrica70','felakutitheafrica70'],'dangelo':['dangeloandthevanguard'],'brucespringsteen':['brucespringsteenandtheestreetband','brucespringsteentheestreetband'],'johncoltrane':['thejohncoltranequartet'],'tobyfox':['tobyradiationfox'],'alicecoltrane':['alicecoltranefeaturingpharoahsanders'],'miltonnascimento':['miltonnascimentoandloborges','miltonnascimentoloborges'],'stangetz':['stangetzandjoaogilberto','stangetzjoaogilberto'],'steveriech':[],'stevereich':['stevereichandmusicians'],'ludwigvanbeethoven':['herbertvonkarajan','berlinerphilharmoniker'],'floatingpoints':['floatingpointspharoahsandersandthelondonsymphonyorchestra'],'dangermouseandblackthought':['dangermouse','blackthought'],'borisandmerzbow':['boriswithmerzbow'],'boriswithmerzbow':['borisandmerzbow'],'boredoms':['boadamusu'],'simonandgarfunkel':['simongarfunkel'],'charlesmingus':['mingus'],'godspeedyoublackemperor':['godspeedyoublackemperor','godspeedyoublackemperor'],'thevelvetunderground':['thevelvetunderground','thevelvetundergroundandnico'],'mybloodyvalentine':[],'ajj':['andrewjacksonjihad'],'travisscott':['travisscott','travisscott'],'lilwayne':['lilwayne'],
 'bobmarleyandthewailers':['bobmarley'],'larryjuneandthealchemist':['larryjune','thealchemist'],
 'freddiegibbsandmadlib':['freddiegibbs','madlib'],'theworldisabeautifulplaceandiamnolongerafraidtodie':['theworldisabeautifulplaceiamnolongerafraidtodie','twiabp'],
 'mfdoom':['mfdoom','doom'],'blink182':['blink182']}
apc=df.an.value_counts()
art_name=df.groupby('an').artist.agg(lambda s:s.value_counts().index[0])
def artist_keys(a):
    n=norm(a); return [n]+alias.get(n,[])
abp=df.groupby(['an','bn']).size()
out=[];drop=[]
for p in PICKS:
    ks=artist_keys(p['artist'])
    ap=int(sum(apc.get(k,0) for k in ks))
    bn=norm(p['album'])
    _alts=p.get('alts','')
    _al=[x for x in _alts.lstrip('=').split(',') if x]
    _ae=(bn==norm(p['artist'])) or len(bn)<6 or bool(re.search(r'(ii|iii|iv|vol\d)$',bn))
    p['m']=[ks,bn,_al,'ae' if (_ae and not _al) else 'ex' if _alts.startswith('=') else 'px']
    alp=0
    for k in ks:
        if k in abp.index.get_level_values(0):
            sub=abp.loc[k]
            alts=p.get('alts','')
            exact=alts.startswith('=')
            al=[x for x in alts.lstrip('=').split(',') if x]
            auto_exact = (bn==norm(p['artist'])) or len(bn)<6 or bool(re.search(r'(ii|iii|iv|vol\d)$',bn))
            for b,c in sub.items():
                if auto_exact and not al:
                    if b==bn: alp+=int(c)
                    continue
                if exact:
                    if b in al: alp+=int(c)
                    continue
                if b in al: alp+=int(c); continue
                if b and (b==bn or (len(bn)>=5 and (b.startswith(bn) or bn.startswith(b) and len(b)>=6))): alp+=int(c)
    tracks=0; first=last=None
    if ap:
        m=df[df.an.isin(ks)]
        tracks=m.track.nunique(); first=int(m.uts.min()); last=int(m.uts.max())
        top=m.track.value_counts().head(3)
        p['topTracks']=[[t,int(c)] for t,c in top.items()]
    p.update(artistPlays=ap,albumPlays=alp,distinctTracks=tracks,first=first,last=last)
    anc=[]
    for a in p['anchors']:
        c=int(sum(apc.get(k,0) for k in artist_keys(a)))
        if c>0 and norm(a) not in ks: anc.append([art_name.get(norm(a),a),c])
    anc.sort(key=lambda x:-x[1]); p['anchors']=anc
    # status
    p['rawStatus']='lived' if alp>=40 else 'heard' if alp>0 else 'artist' if ap>0 else 'never'
    if alp>=40: p['status']='lived'; drop.append(p); continue
    if ap==0: p['status']='new'
    elif ap<15: p['status']='dabbled'
    else: p['status']='fullalbum' if alp<15 else 'revisit'
    out.append(p)
print(len(out),'kept;',len(drop),'already lived in:',[(d['artist'],d['album'],d['albumPlays']) for d in drop])
print(Counter(p['status'] for p in out))
print([(p['artist'],p['album'],p['artistPlays'],p['albumPlays']) for p in out if p['status'] in('fullalbum','revisit')])
rym=sorted([dict(rank=p['rymRank'],rating=p['rymRating'],artist=p['artist'],album=p['album'],st=p['rawStatus'],ap=p['albumPlays'],arp=p['artistPlays']) for p in out+drop if 'rymRank' in p],key=lambda x:x['rank'])
print('RYM',len(rym),Counter(x['st'] for x in rym))
for x in rym:
    if x['rank']>78 and x['st'] in ('lived','heard'): print(x['rank'],x['artist'],x['album'],x['st'],x['ap'],x['arp'])
json.dump(dict(baseUts=int(df.uts.max()),picks=out,rym=rym,lived=[dict(artist=d['artist'],album=d['album'],plays=d['albumPlays']) for d in drop],
  through=str(pd.to_datetime(df.uts.max(),unit='s',utc=True).tz_convert('America/New_York').date()),total=len(df)),open('data.json','w'))
