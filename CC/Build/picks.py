# artist | album | year | lane | canon(1/0) | anchors (his artists) | why | home tag
P = r"""
American Football|American Football|1999|Emo revival 1.0|1|Tigers Jaw;Modern Baseball;Turnover|The twinkly blueprint. "Never Meant" is the door, the other eight songs are the house.|
Cap'n Jazz|Analphabetapolothology|1998|Emo revival 1.0|0|Origami Angel;Prince Daddy & The Hyena;Algernon Cadwallader|Chaotic, yelpy, fast. Basically where Origami Angel's energy comes from.|
The Promise Ring|Nothing Feels Good|1997|Emo revival 1.0|0|Joyce Manor;Modern Baseball;oso oso|Poppy 90s emo with hooks. Easy entry if the screamy stuff isn't the mood.|
Braid|Frame & Canvas|1998|Emo revival 1.0|0|Algernon Cadwallader;Tiny Moving Parts;Mom Jeans.|Dueling vocals and angular guitars. Every revival band owes this one rent.|
Sunny Day Real Estate|Diary|1994|Emo revival 1.0|1|Title Fight;Citizen;Tigers Jaw|Second-wave emo's founding text. Bigger and grungier than you'd expect.|
Mineral|The Power of Failing|1997|Emo revival 1.0|0|Title Fight;Pinegrove;Sorority Noise|Slow builds that blow open. A cornerstone on RYM's emo charts.|
Jawbreaker|24 Hour Revenge Therapy|1994|Emo revival 1.0|1|The Wonder Years;Joyce Manor;Jeff Rosenstock|Pop punk with a notebook full of grudges. Gravelly and endlessly quotable.|
The Get Up Kids|Something to Write Home About|1999|Emo revival 1.0|0|Real Friends;The Story So Far;Knuckle Puck|The bridge between 90s emo and every Warped band you played to death.|
Texas Is the Reason|Do You Know Who You Are?|1996|Emo revival 1.0|0|Title Fight;Citizen;Tigers Jaw|One perfect album and done. Big, clean, earnest guitars.|
Rites of Spring|Rites of Spring|1985|Emo revival 1.0|0|Title Fight;Algernon Cadwallader|Where the word "emo" started. Short, raw, historically mandatory.|
Algernon Cadwallader|Some Kind of Cadwallader|2008|Emo revival 1.0|0|Mom Jeans.;Modern Baseball;Tiny Moving Parts|Philly DIY revival ground zero. You know the band, now sit with the record.|philly
Snowing|I Could Do Whatever I Wanted If I Wanted|2011|Emo revival 1.0|0|Algernon Cadwallader;Origami Angel;Prince Daddy & The Hyena|Pennsylvania basement emo at its most unhinged and fun.|philly
The Hotelier|Home, Like Noplace Is There|2014|Emo revival 1.0|0|Modern Baseball;Sorority Noise;Tigers Jaw|A top-rated revival record on RYM. Heavy subject matter, huge payoff.|
The World Is a Beautiful Place & I Am No Longer Afraid to Die|Whenever, If Ever|2013|Emo revival 1.0|0|Pinegrove;Sorority Noise;Mineral|Emo meets post-rock, many members, big crescendos.|
Empire! Empire! (I Was a Lonely Estate)|You Will Eventually Be Forgotten|2011|Emo revival 1.0|0|American Football;Turnover;Into It. Over It.|Revival-era twinkle with real heartbreak in it.|
Dikembe|Broad Shoulders|2012|Emo revival 1.0|0|Title Fight;Tigers Jaw;Citizen|Grungy revival record that fans of the Title Fight lane swear by.|
Into It. Over It.|Proper|2011|Emo revival 1.0|0|Modern Baseball;Pinegrove;Turnover|Evan Weiss at his most hook-forward. You've got 35 plays of the band, not the record.|
Title Fight|Floral Green|2012|Emo revival 1.0|0|Title Fight;Basement;Turnover|The pivot from pop punk to shoegaze-y emo. Kingston, PA, a short drive from you.|philly
Pianos Become the Teeth|Keep You|2014|Emo revival 1.0|0|Turnover;Title Fight;Sorority Noise|A screamo band that stopped screaming and got devastating.|
Pity Sex|Feast of Love|2013|Indie emo|0|Turnover;Title Fight;Kississippi|Fuzzy, boy-girl shoegaze emo. Sits right next to Turnover's Peripheral Vision.|
Basement|Colourmeinkindness|2012|Emo revival 1.0|0|Title Fight;Turnover;Citizen|UK band, 90s alt-rock grit. Run Ross Run Ross Run.|
La Dispute|Somewhere at the Bottom of the River Between Vega and Altair|2008|Emo revival 1.0|0|Hot Mulligan;Pianos Become the Teeth;Real Friends|Spoken-scream storytelling from Grand Rapids. A Michigan record, just not the rap kind.|
Foxing|The Albatross|2013|Emo revival 1.0|0|Sorority Noise;Turnover;Pinegrove|Slow, cinematic, trumpet and all.|
Cursive|Domestica|2000|Emo revival 1.0|0|Modern Baseball;The Front Bottoms;AJJ|A breakup concept album that yells. RYM regulars rank it near the top of the genre.|
mewithoutYou|Brother, Sister|2006|Emo revival 1.0|0|Pinegrove;AJJ;Sorority Noise|Philly band, half post-hardcore, half spoken folk sermon. Nothing else sounds like it.|philly
Brand New|The Devil and God Are Raging Inside Me|2006|Scene kid (2000s)|1|Real Friends;The Wonder Years;Panic! at the Disco|The scene kid record that critics and RYM both crown. Darker than Deja Entendu.|
Brand New|Deja Entendu|2003|Scene kid (2000s)|0|All Time Low;Fall Out Boy;The Story So Far|The sharp-tongued, hooky Brand New. Long Island scene peak.|
Movements|Feel Something|2017|Warped Tour pop punk (2010s)|0|Real Friends;Knuckle Puck;Moose Blood|Warped-era emo with a spoken-word streak. "Daylily" is the hook.|
Citizen|Youth|2013|Emo revival 1.0|0|Title Fight;Turnover;Basement|Grungy Run For Cover classic. You barely know this band.|
Awakebutstillinbed|what people call low self-esteem is really just seeing yourself the way that other people see you|2015|DIY emo|0|Sweet Pill;Equipment;hospital bracelet|Raw screamed-and-sung DIY emo. Shannon Taylor's voice does the heavy lifting.|
Pool Kids|Pool Kids|2022|Emo revival 2.0|0|Sweet Pill;Origami Angel;Hot Mulligan|Tight, mathy, poppy. Fits right between Sweet Pill and Origami Angel.|
Sincere Engineer|Bless My Psyche|2019|Emo revival 2.0|0|The Front Bottoms;Mom Jeans.;Jeff Rosenstock|Gravel-voiced Chicago pop punk with jokes and dread in equal parts.|
Charmer|Ivy|2019|Emo revival 2.0|0|Prince Daddy & The Hyena;Hot Mulligan;Retirement Party|Michigan emo revival 2.0. Loud, sad, and fun.|
Free Throw|Those Days Are Gone|2014|Emo revival 2.0|0|Hot Mulligan;Mom Jeans.;Tiny Moving Parts|Nashville emo built for screaming along in a car.|
Glass Beach|the first glass beach album|2019|Emo revival 2.0|0|Origami Angel;100 gecs;Prince Daddy & The Hyena|Emo, jazz chords and chiptune in one record. The cleanest bridge from your emo lane to your hyperpop lane.|
Weatherday|Come Dream with Me|2019|DIY emo|0|Equipment;Ogbert the Nerd;hospital bracelet|A bedroom-recorded RYM obsession. Blown-out and huge.|
Home Is Where|i became birds|2021|DIY emo|0|Equipment;Worst party ever;AJJ|Folk punk harmonica plus screamo. Covers two of your lanes at once.|
Carly Cosgrove|See You in Chemistry|2023|Emo revival 2.0|0|Origami Angel;Hot Mulligan;Mom Jeans.|Twinkly, jokey, tight. Fits the emo revival 2.0 crowd exactly.|
Ben Quad|Wish It Were Different|2023|Emo revival 2.0|0|Hot Mulligan;Prince Daddy & The Hyena;Charmer|Michigan-adjacent riffy emo, with big gang vocals.|
Spanish Love Songs|Brave Faces Everyone|2020|Warped Tour pop punk (2010s)|0|The Wonder Years;Real Friends;The Front Bottoms|For Wonder Years people. Anthemic and very bleak.|
Drug Church|Hygiene|2022|Grab bag|0|Title Fight;Turnstile;Basement|Hardcore that's mostly hooks. If GLOW ON hit, try this.|
Death Cab for Cutie|Transatlanticism|2003|Indie|1|The 1975;Turnover;Phoebe Bridgers|Indie canon that taught a whole generation to be sad politely.|
The Microphones|The Glow Pt. 2|2001|Indie|0|Alex G;Pinegrove;Mac DeMarco|A RYM all-timer. Lo-fi, oceanic, strange. Give it a full sit.|
Neutral Milk Hotel|In the Aeroplane Over the Sea|1998|Old rock appreciation|1|AJJ;The Front Bottoms;Alex G|The RYM indie canon. You've touched it, now finish it front to back.|
Modest Mouse|The Lonesome Crowded West|1997|Indie|1|The Front Bottoms;Pinegrove;Mac DeMarco|Jittery, sprawling, angry indie rock. A RYM favorite.|
Built to Spill|Keep It Like a Secret|1999|Indie|0|Turnover;Pavement;Alex G|Guitar-hero indie. Long solos that actually earn it.|
Car Seat Headrest|Twin Fantasy (Face to Face)|2018|Indie|0|Modern Baseball;The Front Bottoms;Alex G|Rambling, cathartic indie. Big with the emo-adjacent crowd on RYM.|
Duster|Stratosphere|1998|Indie|0|Turnover;Alex G;Mac DeMarco|Slowcore that blew up with TikTok kids. Hazy and very easy to live in.|
Elliott Smith|Either/Or|1997|Indie|1|Phoebe Bridgers;Alex G;Soccer Mommy|Hushed, double-tracked, devastating. Phoebe's whole thing starts here.|
Bright Eyes|Lifted or The Story Is in the Soil, Keep Your Ear to the Ground|2002|Indie|0|The Front Bottoms;AJJ;Phoebe Bridgers|Conor Oberst unraveling over strings. Front Bottoms DNA all over it.|
Say Anything|...Is a Real Boy|2004|Scene kid (2000s)|0|The Front Bottoms;Real Friends;Panic! at the Disco|Neurotic, wordy, theatrical pop punk. A scene-kid classic you skipped.|
Manchester Orchestra|Mean Everything to Nothing|2009|Indie emo|0|Kississippi;Turnover;The Wonder Years|Southern-fried emo rock with a big voice.|
Hop Along|Painted Shut|2015|Indie|0|Kississippi;Soccer Mommy;Pinegrove|Philly. Frances Quinlan's voice cracks in the best way.|philly
Japanese Breakfast|Jubilee|2021|Indie|0|Soccer Mommy;HAIM;Phoebe Bridgers|Bright, big indie pop. The band came up in Philly.|philly
Alvvays|Blue Rev|2022|Indie|0|Soccer Mommy;Pity Sex;Snail Mail|Fuzzy jangle pop with a top-rated-of-the-decade case on RYM.|
Big Thief|Capacity|2017|Indie|0|Phoebe Bridgers;Pinegrove;Soccer Mommy|Folk-rock that hits hard and quiet. Fans of Phoebe nearly always land here.|
Mitski|Bury Me at Makeout Creek|2014|Indie|0|Phoebe Bridgers;Soccer Mommy;Snail Mail|Short, loud, raw. Before the big pop records.|
Wednesday|Rat Saw God|2023|Indie|0|Kississippi;Pinegrove;Alex G|Shoegaze-country from North Carolina. A recent RYM favorite.|
Wilco|Yankee Hotel Foxtrot|2002|Old rock appreciation|1|Pinegrove;Big Thief;Grateful Dead|Americana meets static. Pinegrove grew out of this sound.|
Hovvdy|Cranberry|2019|Indie emo|0|Pinegrove;Turnover;Slaughter Beach, Dog|Soft, warm, easy any time of day. Very much your "indie emo" lane.|
Real Estate|Days|2011|Indie|0|Turnover;Mac DeMarco;Pinegrove|Jangly, sunny guitar pop from Ridgewood, NJ.|jersey
Beach House|Teen Dream|2010|Indie|0|Turnover;Clairo;Mac DeMarco|Dream pop's modern standard. Great for late-night drives.|
Arctic Monkeys|Whatever People Say I Am, That's What I'm Not|2006|Indie|1|The Strokes;Two Door Cinema Club;The 1975|Fast, funny, very British. Their scrappy debut, before AM.|
Fleet Foxes|Fleet Foxes|2008|Indie|0|Pinegrove;Big Thief;Noah Kahan|Harmonies for days. A good one to put on with the trop.|
The National|Boxer|2007|Indie|0|The 1975;Phoebe Bridgers;Manchester Orchestra|Baritone dad rock with real tension under it.|
Sufjan Stevens|Carrie & Lowell|2015|Indie|1|Phoebe Bridgers;Pinegrove;Elliott Smith|Quiet grief record. One of the most loved albums of the 2010s.|
Bon Iver|For Emma, Forever Ago|2007|Indie|1|Pinegrove;Phoebe Bridgers;Noah Kahan|The cabin record. Falsetto and acoustic guitar, nothing extra.|
Phoenix|Wolfgang Amadeus Phoenix|2009|Indie|0|Two Door Cinema Club;Vampire Weekend;The 1975|Peak blog-era indie. "1901" and "Lisztomania" are only the start.|
MGMT|Oracular Spectacular|2007|Indie|0|Two Door Cinema Club;Vampire Weekend;Hippo Campus|You know the three singles. The rest is weirder and better.|
Tame Impala|Currents|2015|Indie|1|Mac DeMarco;The 1975;Thundercat|Psych-pop that crossed into everyone's rotation.|
Radiohead|OK Computer|1997|Old rock appreciation|1|The Smiths;The Cure;Weezer|The consensus pick for best album of the 90s. You've barely touched Radiohead.|
Radiohead|In Rainbows|2007|Old rock appreciation|1|The 1975;Turnover;Mac DeMarco|Their warmest record. Easier entry than OK Computer.|
The Cure|Disintegration|1989|Old rock appreciation|1|The Smiths;Turnover;Title Fight|The goth-pop masterpiece. Long, lush, sad.|
Joy Division|Unknown Pleasures|1979|Old rock appreciation|1|The Smiths;The Cure;Title Fight|Cold, spare post-punk. The cover's on half the shirts at any emo show.|
Pixies|Doolittle|1989|Old rock appreciation|1|Nirvana;Weezer;The Front Bottoms|Loud-quiet-loud before Nirvana borrowed it.|
Talking Heads|Remain in Light|1980|Old rock appreciation|1|Vampire Weekend;The 1975;Steely Dan|Afrobeat grooves under new wave. Vampire Weekend's favorite homework.|
The Replacements|Let It Be|1984|Old rock appreciation|0|The Wonder Years;Jawbreaker;The Menzingers|Drunk, sweet, sloppy. The grandfather of every sad punk band you like.|
My Bloody Valentine|Loveless|1991|Old rock appreciation|1|Title Fight;Turnover;Pity Sex|The shoegaze bible. Title Fight's Hyperview lives here.|
Slowdive|Souvlaki|1993|Old rock appreciation|0|Turnover;Title Fight;Beach House|Gentler shoegaze. Pure atmosphere.|
The Velvet Underground|The Velvet Underground & Nico|1967|Appreciating the greats|1|The Strokes;The Smiths;Alex G|Everyone who started a band in the last 50 years heard this first.|
Pavement|Crooked Rain, Crooked Rain|1994|Old rock appreciation|1|Alex G;Mac DeMarco;Turnover|Slacker rock with great melodies. You've got 36 plays, not the full album.|
Weezer|Pinkerton|1996|Old rock appreciation|0|The Front Bottoms;Real Friends;Modern Baseball|The record every emo band calls their favorite.|
R.E.M.|Murmur|1983|Old rock appreciation|0|The Smiths;Pavement;Real Estate|Mumbled, jangly, mysterious. Where indie rock gets its jangle.|
Sonic Youth|Daydream Nation|1988|Old rock appreciation|0|Nirvana;Title Fight;Pavement|Noise rock at its most epic. Long and worth it.|
New Order|Power, Corruption & Lies|1983|Old rock appreciation|0|The Smiths;The Cure;The 1975|Joy Division survivors learn to dance. The 1975 are all over this.|
Jeff Buckley|Grace|1994|Old rock appreciation|1|The Smiths;Radiohead;Manchester Orchestra|One studio album, one of the great voices.|
The Stone Roses|The Stone Roses|1989|Old rock appreciation|0|The Smiths;Oasis;The 1975|Manchester jangle with a groove. The Smiths' cooler cousins.|
Cocteau Twins|Heaven or Las Vegas|1990|Old rock appreciation|0|Beach House;Turnover;Clairo|Dream pop's crown jewel. Lyrics barely matter, which is the point.|
The Smashing Pumpkins|Siamese Dream|1993|Old rock appreciation|1|Title Fight;Turnover;Nirvana|Wall-of-guitar 90s alt. Corgan is half of emo's guitar tone.|
Steely Dan|Aja|1977|Appreciating the greats|1|Steely Dan;Thundercat;Grateful Dead|Their sleekest record. Headphone music, start to finish.|
Fleetwood Mac|Rumours|1977|Appreciating the greats|1|HAIM;The 1975;Harry Styles|The breakup album everyone agrees on. Great with the trop.|
Stevie Wonder|Songs in the Key of Life|1976|Appreciating the greats|1|Thundercat;Anderson .Paak;Childish Gambino|Two hours of peak Stevie. Awaken, My Love! drinks from this well.|
Marvin Gaye|What's Going On|1971|Appreciating the greats|1|Frank Ocean;SZA;Stevie Wonder|Soul's great protest record. Flows as one piece.|
The Beach Boys|Pet Sounds|1966|Appreciating the greats|1|The Beatles;Fleet Foxes;Vampire Weekend|The harmonies everyone keeps borrowing.|
The Beatles|Abbey Road|1969|Appreciating the greats|1|The Beatles;Paul McCartney;Grateful Dead|The side-two medley is the reason to play it front to back.|
The Beatles|Revolver|1966|Appreciating the greats|1|The Beatles;Tame Impala;The Beach Boys|The pivot from pop band to studio wizards.|
Pink Floyd|Wish You Were Here|1975|Appreciating the greats|1|Grateful Dead;Steely Dan;Radiohead|Five songs, all mood. Easier than Dark Side to love.|
Pink Floyd|The Dark Side of the Moon|1973|Appreciating the greats|1|Grateful Dead;Steely Dan;Radiohead|The one album nearly everyone owns. A natural first rip for your library.|
Grateful Dead|American Beauty|1970|Appreciating the greats|1|Grateful Dead;Fleet Foxes;Wilco|The Dead's tight, folky studio peak. "Ripple," "Box of Rain," "Sugar Magnolia."|
Grateful Dead|Workingman's Dead|1970|Appreciating the greats|0|Grateful Dead;Kacey Musgraves;Wilco|American Beauty's twin. Country-folk Dead.|
Bob Marley & The Wailers|Exodus|1977|Appreciating the greats|1|Bob Marley & The Wailers;YG Marley;Michael Franti & Spearhead|Side two is the greatest hits you already know. Side one is the reason to own it.|
Toots & The Maytals|Funky Kingston|1973|Appreciating the greats|0|Bob Marley & The Wailers;YG Marley|Rocksteady joy. The Marley fan's next step.|
Led Zeppelin|Led Zeppelin IV|1971|Appreciating the greats|1|Grateful Dead;Nirvana;The Smashing Pumpkins|Pure classic-rock canon.|
Prince|Purple Rain|1984|Appreciating the greats|1|The Weeknd;Michael Jackson;Thundercat|The rock-funk peak. "Purple Rain" closing it is still undefeated.|
David Bowie|The Rise and Fall of Ziggy Stardust and the Spiders from Mars|1972|Appreciating the greats|1|My Chemical Romance;The Smiths;Panic! at the Disco|Glam concept album. The Black Parade's spiritual dad.|
Joni Mitchell|Blue|1971|Appreciating the greats|1|Phoebe Bridgers;Big Thief;HAIM|Confessional songwriting's high-water mark.|
Bob Dylan|Blood on the Tracks|1975|Appreciating the greats|1|Bright Eyes;Grateful Dead;Noah Kahan|Dylan's breakup record. The most listenable entry point.|
Neil Young|Harvest|1972|Appreciating the greats|1|Grateful Dead;Wilco;Noah Kahan|Soft-rock Neil. Pairs with American Beauty.|
The Allman Brothers Band|At Fillmore East|1971|Appreciating the greats|0|Grateful Dead|If you like the Dead jamming, this is the other half of that world.|
The Band|The Band|1969|Appreciating the greats|0|Grateful Dead;Wilco;Fleet Foxes|Roots-rock at its most lived-in.|
Michael Jackson|Off the Wall|1979|Appreciating the greats|1|Michael Jackson;The Weeknd;Earth, Wind & Fire|Disco-era MJ. Arguably better front to back than Thriller.|
Donald Fagen|The Nightfly|1982|Appreciating the greats|0|Steely Dan|Steely Dan's singer goes solo and stays immaculate.|
The Doobie Brothers|Minute by Minute|1978|Appreciating the greats|0|Steely Dan;Michael Jackson|Yacht rock's core text. Michael McDonald at his smoothest.|
Bruce Springsteen|Born to Run|1975|Appreciating the greats|1|The Wonder Years;The Menzingers;The Gaslight Anthem|Jersey's scripture. Every Jersey punk band you like is chasing this record.|jersey
Nas|Illmatic|1994|Old rap|1|A Tribe Called Quest;Joey Bada$$;Earl Sweatshirt|Ten songs, no misses. The consensus best rap album.|
OutKast|Aquemini|1998|Old rap|1|OutKast;Childish Gambino;Chance the Rapper|Southern, funky, strange. Gambino's Awaken, My Love! comes partly from here.|
Wu-Tang Clan|Enter the Wu-Tang (36 Chambers)|1993|Old rap|1|A Tribe Called Quest;Nas;Joey Bada$$|Grimy, kung-fu, nine voices. The posse cut era starts here.|
A Tribe Called Quest|The Low End Theory|1991|Old rap|1|A Tribe Called Quest;Thundercat;Earl Sweatshirt|Jazz basslines and cool. You like Tribe, so make sure you've done this one front to back.|
The Notorious B.I.G.|Ready to Die|1994|Old rap|1|Nas;JAY-Z;Drake|The storytelling benchmark.|
JAY-Z|The Blueprint|2001|Old rap|1|Drake;Kanye West;JAY-Z|Soul samples and peak Hov. Kanye's production breakout.|
Madvillain|Madvillainy|2004|Alt rap|1|Earl Sweatshirt;Tyler, The Creator;MF DOOM|A RYM top-10 album, all time. Earl and Tyler worship it.|
MF DOOM|Mm..Food|2004|Alt rap|0|Earl Sweatshirt;Tyler, The Creator;BADBADNOTGOOD|Silly, food-themed, brilliant. The friendliest DOOM entry.|
Lauryn Hill|The Miseducation of Lauryn Hill|1998|R&B|1|SZA;Frank Ocean;Kehlani|Rap and soul at once. SZA has called it a direct influence.|
Three 6 Mafia|Mystic Stylez|1995|Old rap|0|Playboi Carti;Ski Mask the Slump God;Lil Uzi Vert|Memphis horrorcore. Half of SoundCloud rap sampled it.|
UGK|Ridin' Dirty|1996|Old rap|0|Future;Young Thug;Drake|Southern rap classic. Slow, soulful, Texan.|
Clipse|Hell Hath No Fury|2006|Old rap|0|Kendrick Lamar;JAY-Z;Earl Sweatshirt|Icy Neptunes beats, venomous verses.|
Lil Wayne|Tha Carter II|2005|Old rap|0|Lil Wayne;Drake;Young Thug|Pre-superstar Wayne, hungriest he ever sounded.|
Eminem|The Marshall Mathers LP|2000|Michigan|1|Big Sean;BabyTron;Danny Brown|Detroit's biggest rap export. The Michigan lane starts here, technically.|
J Dilla|Donuts|2006|Michigan|1|Earl Sweatshirt;Thundercat;BADBADNOTGOOD|Detroit's beat-making god. 31 tracks, one sitting.|
Slum Village|Fantastic, Vol. 2|2000|Michigan|0|A Tribe Called Quest;J Dilla|Detroit's Tribe. Dilla on the boards.|
Danny Brown|Atrocity Exhibition|2016|Michigan|0|Danny Brown;Earl Sweatshirt;BROCKHAMPTON|Detroit's weirdest. You play Danny, but probably not the deep album.|
Danny Brown|XXX|2011|Michigan|0|Danny Brown;Mac Miller;Chance the Rapper|Party half, depressed half. Blog-era Detroit classic.|
ZelooperZ|Van Gogh's Left Ear|2022|Michigan|0|Danny Brown;BabyTron;Earl Sweatshirt|Detroit art-rap from Danny Brown's circle. RYM loved this one.|
Veeze|Ganger|2023|Michigan|0|BabyTron;Babyface Ray;YN Jay|Detroit's laziest flow, in the best way. The Michigan record that broke out nationally.|
Babyface Ray|FACE|2022|Michigan|0|BabyTron;Babyface Ray;RTB MB|Detroit's mellow kingpin. More plays on the album, less on singles.|
Sada Baby|Bartier Bounty|2019|Michigan|0|BabyTron;YN Jay;Rio Da Yung OG|Detroit dance-rap energy. The "Whole Lotta Choppas" guy's real run.|
Tee Grizzley|My Moment|2017|Michigan|0|BabyTron;RTB MB;Big Sean|"First Day Out" is the famous one. The tape holds up.|
Xaviersobased|Keep It Goin Xav|2023|Underground|0|Since99;DJ Lucas;Paul|New York underground at its most chopped-up. Huge with the RYM rap kids.|
Lucki|Freewave 3|2019|Underground|0|Since99;DJ Lucas;Lil Tracy|Chicago drugged-out murmur rap. The underground's quiet godfather.|
SahBabii|Squidtastic|2017|SoundCloud|0|Lil Uzi Vert;Pi’erre Bourne;Lil Tecca|Cult classic for the Uzi and Pi'erre crowd. Whimsical and melodic.|
UnoTheActivist|Live Shit/Real Shit|2018|SoundCloud|0|Playboi Carti;Pi’erre Bourne;Lil Uzi Vert|Atlanta weirdo with Carti-era energy.|
Ken Carson|A Great Chaos|2023|SoundCloud|0|Playboi Carti;Lil Uzi Vert;Ski Mask the Slump God|Opium's loudest. If Whole Lotta Red works, this does too.|
Destroy Lonely|If Looks Could Kill|2023|SoundCloud|0|Playboi Carti;Lil Tracy;Trippie Redd|Opium's moodier side. Long, hazy, rockstar posturing.|
Yeat|Up 2 Me|2021|SoundCloud|0|Lil Uzi Vert;Playboi Carti;Lil Tecca|The bell-heavy breakout tape.|
Chief Keef|Finally Rich|2012|SoundCloud|1|Chief Keef;Lil Uzi Vert;Playboi Carti|Drill's founding album. You file Keef under SoundCloud for a reason.|
Lil Peep|Come Over When You're Sober, Pt. 1|2017|SoundCloud|0|Lil Tracy;Juice WRLD;XXXTENTACION|Emo rap at its clearest. Fully your emo-meets-SoundCloud overlap.|
Wicca Phase Springs Eternal|Corinthian|2020|SoundCloud|0|Lil Peep;Lil Tracy;Title Fight|Tigers Jaw-adjacent goth emo rap (Adam was in Tigers Jaw).|
Bladee|Eversince|2016|Hyperpop|0|Bladee;Yung Lean;Ecco2K|The cult Drain Gang tape. You play Bladee a lot; this is the deep end.|
Bladee|Icedancer|2018|Hyperpop|0|Bladee;Ecco2K;Thaiboy Digital|Whitearmor glitter and sad trance. A fan favorite.|
Ecco2K|E|2019|Hyperpop|0|Bladee;Yung Lean;Charli xcx|The most beautiful Drain Gang record. RYM agrees.|
Yung Lean|Warlord|2016|Hyperpop|0|Bladee;Lil Tracy;Lil Peep|Lean's darkest. The sad boy blueprint.|
Jane Remover|Census Designated|2023|Hyperpop|0|cr1tter;Title Fight;Turnover|Hyperpop kid goes full shoegaze. Your hyperpop and emo lanes shake hands.|
underscores|fishmonger|2021|Hyperpop|0|100 gecs;Origami Angel;Glass Beach|Pop punk, hyperpop and emo in one record.|
brakence|hypochondriac|2022|Hyperpop|0|midwxst;Origami Angel;The Front Bottoms|Emo guitars, glitch production, chatty lyrics.|
SOPHIE|Oil of Every Pearl's Un-Insides|2018|Hyperpop|1|Charli xcx;100 gecs;Bladee|The architect of hyperpop. Brutal and gorgeous.|
Machine Girl|WLFGRL|2014|Hyperpop|0|100 gecs;Ski Mask the Slump God;Bladee|Breakcore chaos. Pure adrenaline.|
Charli xcx|Pop 2|2017|Pop|0|Charli xcx;100 gecs;SOPHIE|The mixtape where Charli went fully hyperpop.|
Kendrick Lamar|To Pimp a Butterfly|2015|Mainstream|1|Kendrick Lamar;Thundercat;Anderson .Paak|Jazz, funk and Thundercat basslines. RYM's top rap record.|
Kendrick Lamar|good kid, m.A.A.d city|2012|Mainstream|1|Kendrick Lamar;Drake;J. Cole|A short film in rap form. Best played in order.|
Kanye West|My Beautiful Dark Twisted Fantasy|2010|Mainstream|1|Kanye West;Travis Scott;Kid Cudi|Maximalist peak. Every song is an event.|
Kanye West|Late Registration|2005|Mainstream|0|Kanye West;Chance the Rapper;JAY-Z|Strings and soul samples. The most purely enjoyable Ye.|
Frank Ocean|Blonde|2016|R&B|1|Frank Ocean;SZA;Tyler, The Creator|The most loved album of the 2010s by a lot of measures.|
Frank Ocean|channel ORANGE|2012|R&B|1|Frank Ocean;Tyler, The Creator;The Internet|Warmer and more song-shaped than Blonde.|
Tyler, The Creator|Flower Boy|2017|Alt rap|0|Tyler, The Creator;Frank Ocean;BROCKHAMPTON|The sunny, sincere Tyler.|
Tyler, The Creator|IGOR|2019|Alt rap|0|Tyler, The Creator;Frank Ocean;Kali Uchis|A breakup album in synths and distortion.|
Freddie Gibbs & Madlib|Piñata|2014|Alt rap|0|Earl Sweatshirt;Danny Brown;Joey Bada$$|Gary, Indiana grit over Madlib soul loops.|
JPEGMAFIA|Veteran|2018|Alt rap|0|Danny Brown;BROCKHAMPTON;Earl Sweatshirt|Glitchy, funny, abrasive. Hyperpop-adjacent rap.|
Vince Staples|Summertime '06|2015|Alt rap|0|Earl Sweatshirt;Kendrick Lamar;Joey Bada$$|Long Beach, cold and minimal.|
Isaiah Rashad|The Sun's Tirade|2016|Alt rap|0|Mac Miller;Earl Sweatshirt;Kendrick Lamar|Lazy, warm TDE record. Mac Miller fans live here.|
Noname|Telefone|2016|Alt rap|0|Chance the Rapper;Saba;Mac Miller|Chicago, gentle, quietly heavy. Straight from the Acid Rap world.|
Saba|CARE FOR ME|2018|Alt rap|0|Chance the Rapper;Vic Mensa;Mac Miller|Chicago grief record. One of the best of its year on RYM.|
Smino|blkswn|2017|Alt rap|0|Chance the Rapper;Anderson .Paak;Childish Gambino|Bouncy St. Louis soul rap.|
Injury Reserve|By the Time I Get to Phoenix|2021|Alt rap|0|BROCKHAMPTON;JPEGMAFIA;Danny Brown|Experimental and haunted. A modern RYM classic.|
Kid Cudi|Man on the Moon: The End of Day|2009|Blog-era nostalgia|1|Kid Cudi;KYLE;Childish Gambino|The blog era's emotional center. Pairs with your Skizzy and KYLE plays.|
Denzel Curry|Melt My Eyez See Your Future|2022|Alt rap|0|Ski Mask the Slump God;Earl Sweatshirt;JPEGMAFIA|Ski Mask's old SoundCloud partner, all grown up.|
Little Simz|Sometimes I Might Be Introvert|2021|Female rap|0|Kendrick Lamar;Noname;Saba|Orchestral, British, stunning.|
Missy Elliott|Supa Dupa Fly|1997|Female rap|1|Nicki Minaj;Doja Cat;Timbaland|Timbaland's futurism plus Missy's swagger.|
Doechii|Alligator Bites Never Heal|2024|Female rap|0|Doja Cat;Megan Thee Stallion;Kendrick Lamar|The 2025 Grammy winner for rap album. Agile, funny, theatrical.|
Rico Nasty|Nightmare Vacation|2020|Female rap|0|100 gecs;Ice Spice;Coi Leray|Punk-rap with a 100 gecs feature.|
Megan Thee Stallion|Fever|2019|Female rap|0|Megan Thee Stallion;Latto;GloRilla|Her best tape. Houston swagger.|
Sexyy Red|Hood Hottest Princess|2023|Female rap|0|Ice Spice;GloRilla;Coi Leray|Loud St. Louis party rap.|
The Weeknd|House of Balloons|2011|R&B|1|The Weeknd;PARTYNEXTDOOR;Drake|The original mixtape. Darker than anything he's made since.|
D'Angelo|Voodoo|2000|R&B|1|Thundercat;Anderson .Paak;Childish Gambino|Neo-soul's high point. Loose, sweaty, perfect.|
Erykah Badu|Baduizm|1997|R&B|1|SZA;The Internet;Thundercat|Neo-soul canon. Jazz-rap's kindest cousin.|
Solange|A Seat at the Table|2016|R&B|0|SZA;Frank Ocean;The Internet|Quiet and pointed. A modern RYM R&B favorite.|
Sade|Love Deluxe|1992|R&B|1|SZA;The Weeknd;Frank Ocean|Smooth to the core. Ideal with the trop.|
Daniel Caesar|Freudian|2017|R&B|0|SZA;Frank Ocean;Kehlani|Gospel-tinged slow burns.|
Bryson Tiller|T R A P S O U L|2015|R&B|0|PnB Rock;Tory Lanez;PARTYNEXTDOOR|Trap-R&B blueprint, right next to PnB Rock.|
Silk Sonic|An Evening with Silk Sonic|2021|R&B|0|Anderson .Paak;Thundercat;Bruno Mars|.Paak and Bruno doing 70s soul. Short and fun.|
Lorde|Melodrama|2017|Pop|1|Lorde;Taylor Swift;The 1975|Pop critics' consensus album of the decade.|
Carly Rae Jepsen|E•MO•TION|2015|Pop|0|Charli xcx;Taylor Swift;HAIM|RYM's favorite "pop done right" record.|
Robyn|Body Talk|2010|Pop|0|Charli xcx;Ariana Grande;Calvin Harris|Crying-on-the-dancefloor pop.|
Beyoncé|Lemonade|2016|Pop|1|SZA;Ariana Grande;The Weeknd|Beyoncé's statement album.|
Rina Sawayama|SAWAYAMA|2020|Pop|0|Panic! at the Disco;Charli xcx;Paramore|Nu-metal guitars in a pop record. Built for a scene kid who grew up.|
Olivia Rodrigo|GUTS|2023|Pop|0|Paramore;Taylor Swift;All Time Low|Pop punk crossover with real teeth.|
Chappell Roan|The Rise and Fall of a Midwest Princess|2023|Pop|0|Sabrina Carpenter;Charli xcx;Lorde|Campy, big, very singable.|
Caroline Polachek|Desire, I Want to Turn Into You|2023|Pop|0|Charli xcx;Lorde;PinkPantheress|Art-pop with a crazy-good voice. A recent RYM favorite.|
My Chemical Romance|Three Cheers for Sweet Revenge|2004|Scene kid (2000s)|1|My Chemical Romance;Panic! at the Disco;Fall Out Boy|The vampire-scene-kid peak. Make sure you've done this one in order.|jersey
Taking Back Sunday|Tell All Your Friends|2002|Scene kid (2000s)|0|Real Friends;The Story So Far;All Time Low|The Long Island screamer every pop punk band copied.|
Thursday|Full Collapse|2001|Scene kid (2000s)|0|My Chemical Romance;Pierce the Veil;Title Fight|New Brunswick, NJ. Ten minutes from Milltown.|jersey
The Used|The Used|2002|Scene kid (2000s)|0|My Chemical Romance;Sleeping With Sirens;Pierce the Veil|Bert McCracken screams; you scream back.|
Underoath|They're Only Chasing Safety|2004|Scene kid (2000s)|0|Pierce the Veil;Attack Attack!;I See Stars|Screamo for kids who wore eyeliner to Hot Topic.|
Jimmy Eat World|Clarity|1999|Scene kid (2000s)|1|The Wonder Years;Real Friends;Turnover|The cult emo record before Bleed American made them huge.|
Dashboard Confessional|The Places You Have Come to Fear the Most|2001|Scene kid (2000s)|0|Real Friends;Mayday Parade;Knuckle Puck|Acoustic emo singalongs. "Screaming Infidelities" and the whole room.|
Motion City Soundtrack|Commit This to Memory|2005|Scene kid (2000s)|0|All Time Low;Fall Out Boy;The Front Bottoms|Moog-synth pop punk with anxious lyrics.|
Circa Survive|Juturna|2005|Scene kid (2000s)|0|Pierce the Veil;Mayday Parade;Title Fight|Philly-area post-hardcore with a soaring falsetto.|philly
A Day to Remember|Homesick|2009|Warped Tour pop punk (2010s)|0|All Time Low;State Champs;Neck Deep|Pop punk with breakdowns. Warped's defining combo.|
blink-182|Enema of the State|1999|Scene kid (2000s)|1|All Time Low;State Champs;Neck Deep|Pop punk's most famous album.|
Green Day|Dookie|1994|Old rock appreciation|1|Real Friends;Neck Deep;Weezer|The pop punk big bang.|
New Found Glory|Sticks and Stones|2002|Scene kid (2000s)|0|State Champs;Real Friends;Knuckle Puck|Easycore before easycore. "My Friends Over You."|
The Starting Line|Say It Like You Mean It|2002|Scene kid (2000s)|0|Real Friends;The Story So Far;Man Overboard|Philly-area pop punk. "Best of Me" still holds.|philly
Yellowcard|Ocean Avenue|2003|Scene kid (2000s)|0|All Time Low;Mayday Parade;Real Friends|Violin pop punk. Peak 2003.|
Saves the Day|Through Being Cool|1999|Emo revival 1.0|0|Real Friends;The Wonder Years;Joyce Manor|Princeton, NJ pop punk with snotty heart. Your backyard.|jersey
Lifetime|Hello Bastards|1995|Warped Tour pop punk (2010s)|0|The Story So Far;Knuckle Puck;Joyce Manor|New Brunswick melodic hardcore. Every 2010s pop punk band's secret influence.|jersey
Senses Fail|Let It Enfold You|2004|Scene kid (2000s)|0|Pierce the Veil;I See Stars;Sleeping With Sirens|Ridgewood, NJ screamo. Peak Hot Topic Jersey.|jersey
Titus Andronicus|The Monitor|2010|Indie|0|The Front Bottoms;The Menzingers;Jeff Rosenstock|Glen Rock, NJ punk concept album about the Civil War and New Jersey.|jersey
The Gaslight Anthem|The '59 Sound|2008|Warped Tour pop punk (2010s)|0|The Wonder Years;The Menzingers;The Front Bottoms|New Brunswick punk doing Springsteen. Pure Jersey.|jersey
Bleachers|Gone Now|2017|Pop|0|The 1975;HAIM;Lorde|Jack Antonoff, New Milford, NJ. Jersey with the trop.|jersey
The Menzingers|On the Impossible Past|2012|Warped Tour pop punk (2010s)|0|The Wonder Years;The Front Bottoms;Real Friends|Scranton-turned-Philly punk. Everyone's favorite sad-bar record.|philly
Seaway|Colour Blind|2015|Warped Tour pop punk (2010s)|0|State Champs;Neck Deep;Knuckle Puck|Bright, polished Canadian pop punk.|
Transit|Listen & Forgive|2011|Warped Tour pop punk (2010s)|0|The Story So Far;Real Friends;Man Overboard|Boston pop punk with emo heart.|
Such Gold|Misadventures|2012|Warped Tour pop punk (2010s)|0|Real Friends;Knuckle Puck;The Story So Far|Fast, technical pop punk.|
Handguns|Angst|2014|Warped Tour pop punk (2010s)|0|Real Friends;Knuckle Puck;Man Overboard|York, PA pop punk at full Warped speed.|philly
Hit the Lights|Skip School, Start Fights|2008|Warped Tour pop punk (2010s)|0|All Time Low;The Ready Set;Forever the Sickest Kids|Peak-era fun pop punk.|
Turnstile|GLOW ON|2021|Grab bag|1|Title Fight;Knocked Loose;Drug Church|Hardcore everyone liked, including people who hate hardcore.|
Joyce Manor|Never Hungover Again|2014|Emo revival 1.0|0|Joyce Manor;The Front Bottoms;Modern Baseball|Nineteen minutes, no filler.|
Jeff Rosenstock|WORRY.|2016|Folk punk|0|The Front Bottoms;AJJ;Modern Baseball|Long Island punk with a 10-song closing medley. Front Bottoms fans' holy text.|
The Mountain Goats|Tallahassee|2002|Folk punk|0|AJJ;The Front Bottoms;Bright Eyes|Acoustic short stories about a marriage falling apart. AJJ fans love it.|
Against Me!|Reinventing Axl Rose|2002|Folk punk|0|AJJ;Local News Legend;Jeff Rosenstock|Acoustic punk that started the folk punk boom.|
AJJ|Knife Man|2011|Folk punk|0|AJJ;Local News Legend;The Front Bottoms|You play AJJ a lot. Their noisiest, best record.|
Zach Bryan|American Heartbreak|2022|Country & folk|0|Noah Kahan;Morgan Wallen;Kacey Musgraves|Thirty-four songs of raw Oklahoma country.|
Tyler Childers|Purgatory|2017|Country & folk|0|Zach Bryan;Noah Kahan;Kacey Musgraves|Kentucky bluegrass-country. Sturgill produced it.|
Sturgill Simpson|Metamodern Sounds in Country Music|2014|Country & folk|0|Kacey Musgraves;Grateful Dead;Tyler Childers|Psychedelic outlaw country. Dead fans get it.|
Jason Isbell|Southeastern|2013|Country & folk|1|Noah Kahan;Zach Bryan;The Menzingers|The modern Americana benchmark.|
MJ Lenderman|Manning Fireworks|2024|Country & folk|0|Wednesday;Pinegrove;Alex G|Slacker alt-country. Funny and sad.|
Waxahatchee|Tigers Blood|2024|Country & folk|0|Kississippi;Soccer Mommy;Pinegrove|Katie Crutchfield, Philly scene alumni, doing Americana.|philly
Kacey Musgraves|Golden Hour|2018|Country & folk|1|Kacey Musgraves;HAIM;Harry Styles|Cosmic country pop. Perfect with the trop.|
Daft Punk|Discovery|2001|Blog-era EDM|1|Calvin Harris;Two Door Cinema Club;Skrillex|French house's party album.|
Justice|†|2007|Blog-era EDM|0|Skrillex;Crizzly;Flosstradamus|Distorted electro, blog-era ground zero.|
Porter Robinson|Worlds|2014|Blog-era EDM|0|Skrillex;100 gecs;Origami Angel|The EDM album that emo and hyperpop kids adopted.|
Disclosure|Settle|2013|Blog-era EDM|0|Calvin Harris;Joel Corry;Ariana Grande|UK garage pop. Still sounds new.|
Flume|Flume|2012|Blog-era EDM|0|RL Grime;Skrillex;Calvin Harris|Wonky future bass. Huge 2013 dorm energy.|
Burial|Untrue|2007|Blog-era EDM|0|Bladee;Ecco2K;Thaiboy Digital|Rainy-night London garage. Drain Gang lists it as a touchstone.|
Miles Davis|Kind of Blue|1959|Grab bag|1|Vince Guaraldi Trio;BADBADNOTGOOD;Thundercat|The jazz album, period. A Sunday morning record.|
John Coltrane|A Love Supreme|1965|Grab bag|1|Vince Guaraldi Trio;BADBADNOTGOOD;Thundercat|Four parts, one prayer.|
Vince Guaraldi Trio|Jazz Impressions of Black Orpheus|1962|Grab bag|0|Vince Guaraldi Trio|You play Guaraldi. This is the non-Charlie Brown masterpiece, with "Cast Your Fate to the Wind."|
Nujabes|Modal Soul|2005|Grab bag|0|A Tribe Called Quest;BADBADNOTGOOD;J Dilla|Lofi hip-hop's founding father. Jazz loops and calm.|
Khruangbin|Con Todo El Mundo|2018|Grab bag|0|BADBADNOTGOOD;Thundercat;Mac DeMarco|Global funk grooves. Great with the trop.|
Toby Fox|UNDERTALE Soundtrack|2015|Grab bag|0|Nicholas Britell;Vince Guaraldi Trio;Porter Robinson|A RYM top-rated soundtrack. Chiptune with real heart.|
Deftones|White Pony|2000|Grab bag|1|Title Fight;Turnover;Knocked Loose|Heavy and dreamy at once. Huge with the shoegaze-emo crowd.|
Bad Bunny|Un Verano Sin Ti|2022|Grab bag|1|Bad Bunny;Drake;The Weeknd|You treat Bad Bunny as a grab bag. This is his career-defining one.|
NewJeans|Get Up|2023|Grab bag|0|NewJeans;PinkPantheress;XG|Jersey club K-pop. Short and perfect.|
Harry Styles|Harry's House|2022|Pop|0|The 1975;HAIM;Harry Styles|Peak with-the-trop music. Check if you've done it front to back.|
HAIM|Women in Music Pt. III|2020|Pop|0|HAIM;Fleetwood Mac;The 1975|Their best and loosest.|
Paramore|After Laughter|2017|Scene kid (2000s)|0|Paramore;The 1975;HAIM|Paramore's 80s pop record. Scene kid meets with-the-trop.|
Maggie Rogers|Heard It in a Past Life|2019|Pop|0|HAIM;Lorde;The 1975|Folk-pop for the car.|
Mac Miller|Swimming|2018|Alt rap|0|Mac Miller;Thundercat;Kid Cudi|The best Mac album. Thundercat all over it.|
Mac Miller|Faces|2014|Alt rap|0|Mac Miller;Earl Sweatshirt;Danny Brown|The dark, sprawling mixtape fans rank highest.|
Childish Gambino|"Awaken, My Love!"|2016|Alt rap|0|Childish Gambino;Thundercat;Prince|Funk Gambino. You play Gambino a ton, so confirm this one's in.|
Chance the Rapper|Acid Rap|2013|Alt rap|1|Chance the Rapper;Vic Mensa;Mac Miller|The Chicago mixtape that made Chance. Good to own, as the original never hit streaming the same way.|
Earl Sweatshirt|Some Rap Songs|2018|Alt rap|0|Earl Sweatshirt;MF DOOM;Mac Miller|Twenty-four minutes of dusty, sad, perfect loops.|
Young Thug|Barter 6|2015|Mainstream|0|Young Thug;Gunna;Lil Uzi Vert|Thug at his most melodic and weird.|
Young Thug|JEFFERY|2016|Mainstream|0|Young Thug;Gunna;Lil Uzi Vert|Every song named after a hero. Wyclef's on it.|
Future|DS2|2015|Mainstream|1|Future;Young Thug;Drake|Future's codeine-dark masterpiece.|
Travis Scott|Rodeo|2015|Mainstream|0|Travis Scott;Kid Cudi;Young Thug|The best Travis album front to back.|
Playboi Carti|Die Lit|2018|SoundCloud|1|Playboi Carti;Pi’erre Bourne;Lil Uzi Vert|Pi'erre's beats, Carti's baby voice. Top-rated on RYM.|
Playboi Carti|Whole Lotta Red|2020|SoundCloud|0|Playboi Carti;Ken Carson;Destroy Lonely|Punk-rap vampire record. Opium starts here.|
Lil Uzi Vert|Luv Is Rage 2|2017|SoundCloud|0|Lil Uzi Vert;Playboi Carti;Juice WRLD|Uzi's emo rockstar peak.|
Lil Yachty|Let's Start Here.|2023|Grab bag|0|Lil Yachty;Tame Impala;Pink Floyd|Yachty goes psychedelic rock. Weird, ambitious, good.|
Drake|Take Care|2011|Mainstream|1|Drake;The Weeknd;PARTYNEXTDOOR|Drake's most beloved album.|
SZA|Ctrl|2017|R&B|1|SZA;Frank Ocean;Kehlani|A modern R&B classic.|
J. Cole|2014 Forest Hills Drive|2014|Mainstream|0|J. Cole;Kendrick Lamar;Drake|You list Cole in your mainstream lane but barely play him.|
YG|My Krazy Life|2014|West coast|0|YG;Mustard;Kendrick Lamar|DJ Mustard's peak production, LA gangster storytelling.|
Mac Dre|Thizzelle Washington|2002|West coast|0|Kool John;Iamsu!;E-40|Bay Area legend. "Thizz" culture starts here.|
E-40|In a Major Way|1995|West coast|0|Kool John;Iamsu!;Mac Dre|Vallejo slang machine.|
Larry June & The Alchemist|The Great Escape|2023|West coast|0|Kool John;Iamsu!;Freddie Gibbs & Madlib|San Francisco luxury-chill rap. Big RYM year.|
Kamaiyah|A Good Night in the Ghetto|2016|West coast|0|Iamsu!;YG;Kool John|Oakland party rap. Feels like 2016 Bay.|
Drakeo the Ruler|Thank You for Using GTL|2020|West coast|0|03 Greedo;Mustard;Kool John|LA mumble rap recorded over a jail phone call.|
Asher Roth|Asleep in the Bread Aisle|2009|Blog-era nostalgia|0|Hoodie Allen;Chiddy Bang;Skizzy Mars|Frat-rap origin story. Pennsylvania suburbs.|philly
Wiz Khalifa|Kush & Orange Juice|2010|Blog-era nostalgia|0|Hoodie Allen;Mac Miller;G-Eazy|The blog-era stoner mixtape. Peak 2010.|
Kendrick Lamar|Section.80|2011|Blog-era nostalgia|0|Kendrick Lamar;Joey Bada$$;Mac Miller|Pre-fame Kendrick. A blog-era Kendrick most people skipped.|
Joey Bada$$|1999|2012|Old rap|0|Joey Bada$$;Flatbush ZOMBiES;Earl Sweatshirt|90s boom bap made by a 17-year-old in 2012.|
ScHoolboy Q|Habits & Contradictions|2012|Alt rap|0|Kendrick Lamar;Mac Miller;Earl Sweatshirt|TDE's grimiest. Hazy and menacing.|
"""
PICKS=[]
for line in P.strip().split("\n"):
    a=line.split("|")
    PICKS.append(dict(artist=a[0],album=a[1],year=int(a[2]),lane=a[3],canon=a[4]=="1",anchors=[x for x in a[5].split(";") if x],why=a[6],home=a[7] if len(a)>7 else ""))
print(len(PICKS))
