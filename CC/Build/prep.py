import json,re,math
d=json.load(open('data.json'))
def typo(s): return re.sub(r'"([^"]*)"',r'“\1”',s).replace("'", "’")
def pid(a,b): return re.sub(r'[^a-z0-9]+','-',(a+'-'+b).lower()).strip('-')[:80]
for p in d['picks']:
    p['why']=typo(p['why']); p['dAlbum']=typo(p['album']); p['dArtist']=typo(p['artist'])
    if p.get('topTracks'): p['topTracks']=[[typo(t),c] for t,c in p['topTracks']]
    p['anchors']=[[typo(a),c] for a,c in p['anchors']]
    aff=sum(math.log10(1+c) for _,c in p['anchors'][:3])
    p['score']=round(aff+(1.2 if p['canon'] else 0)+{'new':0.6,'dabbled':0.8,'fullalbum':1.0,'revisit':0.3}[p['status']]+(0.8 if p.get('rymRank') else 0),3)
    p['id']=pid(p['artist'],p['album'])
    for k in ('first','last','distinctTracks','rawStatus','alts'): p.pop(k,None)
for r in d['rym']:
    r['id']=pid(r['artist'],r['album']); r['dAlbum']=typo(r['album']); r['dArtist']=typo(r['artist'])
json.dump(d,open('data2.json','w'),ensure_ascii=False)
print(len(d['picks']),len(d['rym']))
