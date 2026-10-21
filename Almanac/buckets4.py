import pandas as pd, numpy as np, collections
src=open('era.py').read().replace("df['sess']=","df.loc[df.artist=='rip eternal','artist']='Paul'\ndf['sess']=")
exec(src)
B={
'Detroit & plugg underground':"RTB MB|DJ Lucas|YN Jay|Since99|Jay Critch|BabyTron|Lil Tecca|Bfb Da Packman|Rio Da Yung OG|Ice Spice|Papo2oo4|ShittyBoyz|SEBii|Central Cee|Autumn!|Jay Eazy|Punchmade Dev|Brian313|nettspend|twikipedia|Mally Bandz|Rich the Kid|Sha EK|KYLE|midwxst|Weird Dane|Online Tony|Precious Little Life|Cash Kidd|ppcocaine",
'The new wave (2025–26)':"Babyfxce E|Kasher Quon|Cash Cobain|Anycia|Veeze|Danny G Beats|Bay Swag|Latto|StanWill|Bandmanrill|Christ Dillinger|JWU|Laron|LUCY (Cooper B. Handy)|Kay Flock|Xanman|Chow Lee|Phony|GloRilla|Bossman Dlow|Skrilla|Jorjiana|1900rugrat|Ankith Woods|$weet-T|Bktherula|Chanel Yates|KrimeLife Ca$$|Benji Blue Bills|holottacheese|22bb|Cheem",
'Paul (his own lane)':"Paul",
'Hyperpop':"Bladee|Ecco2K|Thaiboy Digital|Yung Lean|cr1tter|poptropicaslutz!|100 gecs|2hollis|ericdoa|Jane Remover|underscores|glaive|brakence|Alice Gas|6arelyhuman",
'Comfort rap':"Lil Uzi Vert|Drake|Pi’erre Bourne|Playboi Carti|NAV|Yeat|PnB Rock|Lil Yachty|Trippie Redd|YoungBoy Never Broke Again|Juice WRLD|Lil Tracy|Gunna|Future|Travis Scott|Aminé|Lil Mosey|CL4PERS|Lil Durk|Young Thug|Pop Smoke|A Boogie wit da Hoodie|Luh Tyler|Lil Baby|Young Nudy|SahBabii|Babyface Ray|Tyler, The Creator|Chance the Rapper|Kodak Black|Baby Keem|JID|Tana|WhatUpNolan|Lucki|Kendrick Lamar|Earl Sweatshirt|Mac Miller|Coi Leray|DD Osama|Quavo|Lil Pump|Metro Boomin|The Kid LAROI|Don Toliver|Famous Dex|Kanye West|J. Cole|XXXTENTACION|Denzel Curry|Lil Skies|Vince Staples|Retro|Dreamville",
'Driving with the trop':"Sabrina Carpenter|Taylor Swift|SZA|Charli xcx|Clairo|Doja Cat|Harry Styles|The 1975|Chappell Roan|Gracie Abrams|Faye Webster|Wallows|Djo|The Beaches|Noah Kahan|Kacey Musgraves|Ariana Grande|PinkPantheress|Addison Rae|Kehlani|Lana Del Rey|John Mayer|Morgan Wallen|Post Malone|Bruno Mars|Remi Wolf|Olivia Rodrigo|Hayley Williams|MUNA|Vampire Weekend|Anderson .Paak|NxWorries|Thundercat|Bebe Rexha|Jack Harlow|Phoenix|HAIM|Weezer|Goo Goo Dolls|The Smashing Pumpkins|Sugar Ray|Vulfpeck|The Japanese House|The Band CAMINO|Waxahatchee|Lil Nas X|Michael Franti & Spearhead|Wuki|Miranda Hope|Nico Segal|Joel Corry|Two Door Cinema Club|Catfish and the Bottlemen|The Backseat Lovers|Billie Eilish|Justin Bieber|Lily Allen|Becky Hill|Calvin Harris|David Guetta|Rema|The Weeknd|Steve Lacy|Charlie Puth|The Aces|Hazel English|Samia|Lyrical Lemonade|NewJeans|KATSEYE",
'Current emo & indie':"Alex G|Mom Jeans.|Pinegrove|Kississippi|Equipment|oso oso|Super American|Prince Daddy & The Hyena|Origami Angel|macseal|fanclubwallet|Ogbert the Nerd|Hot Mulligan|Sweet Pill|Another Michael|Jail Socks|saturdays at your place|Soccer Mommy|Phoebe Bridgers|boygenius|pictures of vernon|Hippo Campus|Palette Knife|Bilmuri|Johnny Football Hero|Small Crush|Ovlov|Snail Mail|Blue Deputy|Worst party ever|Knope|Local News Legend|Slow Pulp|The Beths|Lucy Dacus|Car Seat Headrest|Slaughter Beach, Dog|Beach Bunny|Bay Faction|Your Arms Are My Cocoon|Thank You, I'm Sorry|They Are Gutting a Body of Water|armbite|cashcache!|Riley!|awakebutstillinbed|hospital bracelet",
'Title Fight & Algernon (2010s emo)':"Title Fight|Algernon Cadwallader|Tigers Jaw|Turnover|Glocca Morra|Balance and Composure|Basement|Citizen|Mat Kerekes|Microwave|American Football|Cap'n Jazz|Snowing|Into It. Over It.|The Hotelier|Touché Amoré|La Dispute|Pity Sex|Daylight",
'Warped Tour pop punk (2010s)':"Real Friends|The Story So Far|Knuckle Puck|State Champs|Neck Deep|The Wonder Years|Modern Baseball|The Front Bottoms|Joyce Manor|Just Friends|Mayday Parade|Four Year Strong|Seaway|Candy Hearts|Man Overboard|Fireworks|Movements|Say Anything|The Starting Line|Motion City Soundtrack|blink-182|Broadway|Major League|Transit|Seahaven|With Confidence|Moose Blood|Hit the Lights|Forever Came Calling",
'Scene kid (2000s)':"My Chemical Romance|Paramore|Panic! at the Disco|Fall Out Boy|All Time Low|Breathe Carolina|Pierce the Veil|Sleeping With Sirens|Attack Attack!|Dance Gavin Dance|Asking Alexandria|The Devil Wears Prada|I Set My Friends on Fire|From First to Last|Forever the Sickest Kids|Cute Is What We Aim For|The Ready Set|The Cab|Alesana|Underoath|Bring Me the Horizon|The Used|Escape The Fate|Of Mice & Men|A Skylit Drive|Issues|Sparks The Rescue|Abandon All Ships|The Academy Is...|A Day to Remember|Brokencyde|3OH!3|We The Kings|Boys Like Girls|Cobra Starship|Hey Monday|Metro Station",
'Old rock appreciation':"The Smiths|The Cure|Nirvana|The Cranberries|Radiohead|Pavement|The Strokes|Talking Heads|R.E.M.|Pixies|Joy Division|New Order|Oasis|Blur|Pearl Jam|Foo Fighters|Red Hot Chili Peppers|The Replacements|Sonic Youth|Modest Mouse|Neutral Milk Hotel",
'Appreciating the greats':"Steely Dan|Bob Marley & The Wailers|The Wailers|Grateful Dead|The Beatles|Paul McCartney|Wings|Stevie Wonder|Michael Jackson|Tony Toni Toné|Frank Sinatra|Fleetwood Mac|YG Marley|Earth, Wind & Fire|Marvin Gaye|Bob Dylan|The Rolling Stones|Led Zeppelin|Prince|Al Green|Paul Simon|Simon & Garfunkel|James Taylor|The Beach Boys|Billy Joel|Elton John|Van Morrison|Bill Withers",
}
seed={a:k for k,v in B.items() for a in v.split('|')}
assert all(len(v.split('|'))==len(set(v.split('|'))) for v in B.values())
evc=E.artist.value_counts()
assign=dict((a,k) for a,k in seed.items() if a in evc.index)
# propagate to unseeded artists with >=8 era plays using co-session affinity
import itertools
SS=E.groupby('sess').artist.apply(set)
occ2=collections.Counter(); pair2=collections.Counter()
cand=set(evc[evc>=25].index)
for s in SS:
    s=s&(cand|set(assign))
    for a in s: occ2[a]+=1
    for a,b in itertools.combinations(sorted(s),2): pair2[(a,b)]+=1
def j2(a,b):
    c=pair2.get((a,b) if a<b else (b,a),0); return c/(occ2[a]+occ2[b]-c) if c else 0
prop={}
for a in cand-set(assign):
    sc=collections.defaultdict(list)
    for b,k in assign.items():
        if b in occ2: sc[k].append(j2(a,b))
    best=max(sc,key=lambda k:np.mean(sorted(sc[k],reverse=True)[:3]))
    v=np.mean(sorted(sc[best],reverse=True)[:3])
    if v>=0.08: prop[a]=best
assign.update(prop)
E['bucket']=E.artist.map(assign).fillna('Everything else')
