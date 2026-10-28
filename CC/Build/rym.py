# rank|rating|artist|album|year|lane|canon|anchors|why|alts(norm album alternates, comma)
R = r"""
1|4.37|Kendrick Lamar|To Pimp a Butterfly||||||
2|4.30|Radiohead|OK Computer||||||
3|4.33|Radiohead|In Rainbows||||||
4|4.37|Pink Floyd|Wish You Were Here||||||
5|4.34|King Crimson|In the Court of the Crimson King|1969|Old rock appreciation|0|Pink Floyd;Radiohead;Steely Dan|Prog rock’s big bang. The opener alone will wake you up.|
6|4.32|Kendrick Lamar|good kid, m.A.A.d city||||||
7|4.27|Pink Floyd|The Dark Side of the Moon||||||
8|4.24|Radiohead|Kid A|2000|Old rock appreciation|1|Radiohead;Bladee;Mac DeMarco|Radiohead goes cold and electronic. Bladee fans tend to get it fast.|
9|4.32|Madvillain|Madvillainy||||||
10|4.25|My Bloody Valentine|Loveless||||||
11|4.30|The Beatles|Abbey Road||||||
12|4.26|Talking Heads|Remain in Light||||||
13|4.26|David Bowie|The Rise and Fall of Ziggy Stardust and the Spiders from Mars||||||
14|4.28|Godspeed You! Black Emperor|Lift Yr. Skinny Fists Like Antennas to Heaven!|2000|Grab bag|0|Foxing;The World Is a Beautiful Place & I Am No Longer Afraid to Die;Nicholas Britell|Post-rock’s grand statement. Four long movements that build like a movie score.|liftyourskinnyfistslikeantennastoheaven
15|4.23|The Beatles|Revolver||||||
16|4.27|Nas|Illmatic||||||
17|4.24|Black Sabbath|Paranoid|1970|Old rock appreciation|1|Nirvana;Knocked Loose;Deftones|Heavy metal’s starting point. Short and all riffs.|
18|4.28|Björk|Vespertine|2001|Grab bag|0|Ecco2K;Bladee;Charli xcx|Hushed, glittery electronic pop. Ecco2K is basically a Vespertine kid.|
19|4.26|The Cure|Disintegration||||||
20|4.33|Charles Mingus|The Black Saint and the Sinner Lady|1963|Grab bag|0|Vince Guaraldi Trio;BADBADNOTGOOD;Thundercat|Big-band jazz that swings and lurches. RYM’s top jazz record.|
21|4.19|The Velvet Underground|The Velvet Underground & Nico||||||
22|4.30|John Coltrane|A Love Supreme||||||
23|4.21|Pink Floyd|Animals|1977|Appreciating the greats|0|Pink Floyd;Grateful Dead;Steely Dan|Three long songs about dogs, pigs and sheep. Their angriest record.|
24|4.28|King Crimson|Red|1974|Old rock appreciation|0|Deftones;Title Fight;Radiohead|Heavy, tense prog that sounds decades ahead of 1974.|
25|4.21|Cocteau Twins|Heaven or Las Vegas||||||
26|4.32|Stevie Wonder|Songs in the Key of Life||||||
27|4.24|Miles Davis|Kind of Blue||||||
28|4.20|The Beach Boys|Pet Sounds||||||
29|4.22|Fishmans|Long Season|1996|Grab bag|0|Turnover;Mac DeMarco;Khruangbin|One 35-minute dub-pop song from Tokyo. The classic RYM rabbit hole.|
30|4.11|Tyler, The Creator|IGOR||||||
31|4.08|Kanye West|My Beautiful Dark Twisted Fantasy||||||
32|4.15|Kanye West|The College Dropout|2004|Mainstream|1|Kanye West;Chance the Rapper;JAY-Z|Soul samples and jokes. Chance’s whole style starts here.|
33|4.18|Portishead|Dummy|1994|Grab bag|0|The Weeknd;Beach House;Massive Attack|Trip-hop’s defining record. Smoky and slow.|
34|4.16|Slint|Spiderland|1991|Old rock appreciation|0|Foxing;American Football;Title Fight|Post-rock’s foundation. A lot of midwest emo’s guitar math comes from here.|
35|4.22|Wu-Tang Clan|Enter the Wu-Tang (36 Chambers)||||||
36|4.19|Nick Drake|Pink Moon|1972|Appreciating the greats|0|Elliott Smith;Phoebe Bridgers;Bon Iver|Voice and acoustic guitar, 28 minutes, nothing else.|
37|4.11|Death Grips|The Money Store|2012|Alt rap|0|JPEGMAFIA;Danny Brown;100 gecs|Abrasive noise-rap. JPEGMAFIA and hyperpop both owe it.|
38|4.08|Neutral Milk Hotel|In the Aeroplane Over the Sea||||||
39|4.15|Slowdive|Souvlaki||||||
40|4.13|The Smiths|The Queen Is Dead|1986|Old rock appreciation|1|The Smiths;The Cure;The 1975|The Smiths at their sharpest and funniest.|
41|4.12|The Beatles|Sgt. Pepper's Lonely Hearts Club Band|1967|Appreciating the greats|1|The Beatles;Paul McCartney;The Beach Boys|The concept-album template.|
42|4.18|The Microphones|The Glow Pt. 2||||||
43|4.14|Daft Punk|Discovery||||||
44|4.21|Marvin Gaye|What's Going On||||||
45|4.16|Björk|Homogenic|1997|Grab bag|0|Ecco2K;Charli xcx;SOPHIE|Strings and harsh beats colliding. Björk’s toughest record.|
46|4.14|The Beatles|The Beatles (White Album)|1968|Appreciating the greats|1|The Beatles;Paul McCartney;Grateful Dead|Thirty songs, every direction at once.|=thebeatles,thebeatleswhitealbum,whitealbum
47|4.18|Elliott Smith|Either/Or||||||
48|4.10|Joy Division|Unknown Pleasures||||||
49|4.09|Frank Ocean|Blonde||||||
50|4.17|Godspeed You! Black Emperor|F♯ A♯ ∞|1997|Grab bag|0|Nicholas Britell;Foxing|Bleak, cinematic post-rock. Their debut.|=fainfinity,fsharpasharpinfinity,fa
51|4.23|Miles Davis|In a Silent Way|1969|Grab bag|0|Thundercat;BADBADNOTGOOD;Khruangbin|Fusion’s quiet dawn. Two long, glowing pieces.|
52|4.11|Aphex Twin|Selected Ambient Works 85-92|1992|Blog-era EDM|0|Skrillex;Porter Robinson;Burial|Where electronic music’s soft side starts.|
53|4.16|A Tribe Called Quest|The Low End Theory||||||
54|4.05|Nirvana|Nevermind|1991|Old rock appreciation|1|Nirvana;Weezer;The Smashing Pumpkins|You know the singles. Hear it as an album.|
55|4.19|Yes|Close to the Edge|1972|Old rock appreciation|0|Pink Floyd;Steely Dan;Grateful Dead|Peak prog. One side-long epic and two near-epics.|
56|4.13|Have a Nice Life|Deathconsciousness|2008|Indie|0|Title Fight;Turnover;Weatherday|Bleak shoegaze-goth cult classic that RYM basically made famous.|
57|4.13|Danny Brown|Atrocity Exhibition||||||
58|4.15|David Bowie|★ (Blackstar)|2016|Appreciating the greats|0|Radiohead;Kendrick Lamar;The 1975|Bowie’s jazz-tinged farewell, out two days before he died.|=blackstar
59|4.40|Fishmans|98.12.28 男達の別れ|1999|Grab bag|0|Turnover;Khruangbin;Mac DeMarco|Their farewell live show. The highest average rating in this stretch of the chart.|=981228otokotachinowakare,981228
60|4.14|MF DOOM|Mm..Food||||||
61|4.14|Kate Bush|Hounds of Love|1985|Appreciating the greats|1|Lorde;Caroline Polachek;HAIM|“Running Up That Hill” on side one, a whole suite on side two.|
62|4.13|Jeff Buckley|Grace||||||
63|4.14|Television|Marquee Moon|1977|Old rock appreciation|0|The Strokes;Pavement;The Smiths|Twin-guitar punk-era classic. The Strokes did their homework here.|
64|4.14|Sufjan Stevens|Illinois|2005|Indie|0|Sufjan Stevens;Pinegrove;Fleet Foxes|Big, orchestral, and all about one state.|
65|4.13|David Bowie|Low|1977|Appreciating the greats|0|Radiohead;The Cure;Joy Division|Bowie in Berlin. Half songs, half ambient.|
66|4.07|Nirvana|In Utero|1993|Old rock appreciation|0|Nirvana;Title Fight;Basement|Rawer and meaner than Nevermind.|
67|4.14|Black Sabbath|Master of Reality|1971|Old rock appreciation|0|Knocked Loose;Deftones;Nirvana|Sludgier Sabbath. Stoner rock starts here.|
68|4.15|Bob Dylan|Highway 61 Revisited|1965|Appreciating the greats|1|Grateful Dead;Bright Eyes;The Front Bottoms|Dylan goes electric, opening with “Like a Rolling Stone.”|
69|4.18|Miles Davis|Bitches Brew|1970|Grab bag|0|Thundercat;BADBADNOTGOOD;Khruangbin|Murky electric jazz fusion. Thundercat’s great-grandparent.|
70|4.13|DJ Shadow|Endtroducing.....|1996|Grab bag|0|J Dilla;Nujabes;BADBADNOTGOOD|Built entirely from samples. Pair it with Donuts.|
71|4.04|Black Country, New Road|Ants From Up There|2022|Indie|0|Car Seat Headrest;The Microphones;Sorority Noise|A recent RYM all-timer. Emotional, baroque, huge finish.|
72|4.10|Led Zeppelin|Led Zeppelin IV||||||
73|4.07|Kanye West|Late Registration||||||
74|4.11|Massive Attack|Mezzanine|1998|Grab bag|0|Portishead;The Weeknd;Burial|Dark trip-hop. “Teardrop” is the one you know.|
75|4.15|Swans|Soundtracks for the Blind|1996|Grab bag|0|Nicholas Britell;Have a Nice Life;Godspeed You! Black Emperor|Two-plus hours of drone and dread. The deep end of RYM.|
76|4.14|J Dilla|Donuts||||||
77|4.11|Nine Inch Nails|The Downward Spiral|1994|Old rock appreciation|0|Pierce the Veil;Deftones;Knocked Loose|Industrial rock’s darkest hit record.|
78|4.08|Pixies|Doolittle||||||
"""
RYM=[]
for line in R.strip().split("\n"):
    a=line.split("|")
    RYM.append(dict(rank=int(a[0]),rating=float(a[1]),artist=a[2],album=a[3],year=a[4],lane=a[5],canon=a[6]=="1",anchors=a[7],why=a[8],alts=a[9]))
