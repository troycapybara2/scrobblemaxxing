CL = {
 'classicrock':('Old rock appreciation','Grateful Dead;The Beatles;Led Zeppelin','Classic-rock canon that nearly everyone signs off on.'),
 'prog':('Old rock appreciation','Pink Floyd;Steely Dan;Grateful Dead','Prog canon. Long songs and big ideas, the natural next stop after Floyd.'),
 'jazz':('Grab bag','Vince Guaraldi Trio;BADBADNOTGOOD;Thundercat','A jazz pillar on RYM. Your Guaraldi and BADBADNOTGOOD plays are the way in.'),
 'spiritjazz':('Grab bag','BADBADNOTGOOD;Thundercat;Khruangbin','Spiritual jazz. Long, cosmic and meditative, the kind of thing Thundercat grew up on.'),
 'metal':('Grab bag','Knocked Loose;Deftones;Dying Wish','A metal landmark on RYM. Your Knocked Loose plays are the door.'),
 'deathmetal':('Grab bag','Knocked Loose;Dying Wish;Deftones','Technical death metal. The deep end, even for Knocked Loose fans.'),
 'folk':('Appreciating the greats','Phoebe Bridgers;Bon Iver;Grateful Dead','Songwriting canon. Lyric-first and built to sit with.'),
 'soul':('Appreciating the greats','Thundercat;Stevie Wonder;Anderson .Paak','Soul and funk canon. Where Thundercat and .Paak got their basslines.'),
 'rnb':('R&B','SZA;Frank Ocean;Thundercat','Neo-soul canon. SZA and Frank Ocean both live downstream of it.'),
 'postpunk':('Old rock appreciation','The Smiths;The Cure;Joy Division','Post-punk essential. Your Smiths and Cure plays point right at it.'),
 'punk':('Old rock appreciation','Green Day;Jeff Rosenstock;Title Fight','Punk foundation. Most of what played on Warped Tour traces back here.'),
 'grunge':('Old rock appreciation','Nirvana;Weezer;The Smashing Pumpkins','90s alt-rock essential, right next to your Nirvana and Pumpkins plays.'),
 'indie':('Indie','Alex G;Pavement;Turnover','Indie rock canon. Alex G and Turnover live downstream of it.'),
 'slowcore':('Indie emo','Pinegrove;Alex G;Phoebe Bridgers','Slow, hushed, sad indie. The quiet end of your indie emo lane.'),
 'shoegaze':('Indie','Turnover;Title Fight;Beach House','Dreamy, fuzzed-out guitars. Turnover’s Peripheral Vision lives nearby.'),
 'drone':('Grab bag','Foxing;Nicholas Britell;Deftones','Big, slow and atmospheric. The deep end of RYM.'),
 'kraut':('Old rock appreciation','Radiohead;Talking Heads;Steely Dan','Hypnotic grooves that Radiohead and Talking Heads borrowed from.'),
 'electronic':('Blog-era EDM','Skrillex;Porter Robinson;Calvin Harris','Electronic canon, a step past your blog-era EDM.'),
 'triphop':('Grab bag','The Weeknd;Beach House;Burial','Moody trip-hop. The Weeknd’s early sound owes it a lot.'),
 'goldrap':('Old rap','A Tribe Called Quest;Nas;Joey Bada$$','Golden-era rap essential. Fits right next to your Tribe and Nas plays.'),
 'altrap':('Alt rap','Danny Brown;Earl Sweatshirt;JPEGMAFIA','Left-field rap the RYM crowd swears by. Danny Brown fans start here.'),
 'kanye':('Mainstream','Kanye West;Kid Cudi;Travis Scott','You play Kanye a lot, and this is one RYM still argues about.'),
 'brazil':('Grab bag','Khruangbin;Bad Bunny;Stevie Wonder','Brazilian classic. Warm, rhythmic and gorgeous, no Portuguese required.'),
 'argentina':('Grab bag','Bad Bunny;The Beatles;Radiohead','Argentine rock essential, a fixture near the top of RYM.'),
 'latin':('Grab bag','Bad Bunny;Kacey Musgraves','Latin American classic RYM keeps near the top.'),
 'japan':('Grab bag','Turnover;Khruangbin;NewJeans','A Japanese classic RYM loves. Easier listening than you’d think.'),
 'soundtrack':('Grab bag','Nicholas Britell;Toby Fox;Vince Guaraldi Trio','Soundtrack canon. Your Nicholas Britell plays say you’ll like it.'),
 'classical':('Grab bag','Nicholas Britell;Vince Guaraldi Trio','Classical cornerstone. Put it on and let it run.'),
 'pop':('Pop','Charli xcx;Lorde;The 1975','Pop record the RYM crowd actually rates.'),
 'posthc':('Scene kid (2000s)','Pierce the Veil;Title Fight;Knocked Loose','Post-hardcore landmark. Scene kids’ older siblings swore by it.'),
}
# rank|album|artist|rating|cluster|why ('' = cluster default, '@live' = live-album note)
L = r"""
79|Electric Ladyland|The Jimi Hendrix Experience|4.16|classicrock|
80|The Doors|The Doors|4.09|classicrock|
81|Imaginal Disk|Magdalena Bay|4.10|pop|Synth-pop that RYM crowned in 2024. Charli and Polachek fans, this one’s yours.
82|Station to Station|David Bowie|4.14|classicrock|Bowie’s cocaine-funk record. Six songs, all of them long and strange.
83|Ride the Lightning|Metallica|4.08|metal|
84|Laughing Stock|Talk Talk|4.13|drone|
85|Symbolic|Death|4.15|deathmetal|
86|Blood on the Tracks|Bob Dylan|4.16|folk|
87|Blonde on Blonde|Bob Dylan|4.14|folk|
88|Love Deluxe|Sade|4.16|rnb|
89|Karma|Pharoah Sanders|4.18|spiritjazz|
90|Carrie & Lowell|Sufjan Stevens|4.09|indie|
91|Since I Left You|The Avalanches|4.08|electronic|Built from thousands of samples. A party record and a headphone record at once.
92|Closer|Joy Division|4.07|postpunk|
93|Aquemini|OutKast|4.13|goldrap|
94|Is This It|The Strokes|4.01|indie|The Strokes are in your old rock lane. This is the whole reason.
95|Velocity : Design : Comfort|Sweet Trip|4.08|shoegaze|Glitchy dream pop the internet rediscovered. Sits between your hyperpop and shoegaze-y emo.
96|Clube da Esquina|Milton Nascimento|4.16|brazil|
97|Innervisions|Stevie Wonder|4.15|soul|
98|Black Sabbath|Black Sabbath|4.07|metal|
99|Rubber Soul|The Beatles|4.02|classicrock|
100|Midnight Marauders|A Tribe Called Quest|4.13|goldrap|You love Tribe. Make sure this one’s done front to back too.
101|Stop Making Sense|Talking Heads|4.34|postpunk|@live
102|Master of Puppets|Metallica|4.03|metal|
103|Are You Experienced|The Jimi Hendrix Experience|4.09|classicrock|
104|Songs of Leonard Cohen|Leonard Cohen|4.12|folk|
105|Toxicity|System of a Down|4.04|metal|Nu-metal everyone knows. Scene kids grew up on “Chop Suey!”
106|Pornography|The Cure|4.07|postpunk|The Cure at their darkest. You play them plenty, so try the heavy one.
107|Piñata|Freddie Gibbs & Madlib|4.10|altrap|
108|Thriller|Michael Jackson|4.06|soul|You know every single. Hear it as an album.
109|Rumours|Fleetwood Mac|4.05|classicrock|
110|When the Pawn...|Fiona Apple|4.11|pop|Fiona at her sharpest. Phoebe and Soccer Mommy fans should hear where it comes from.
111|All Things Must Pass|George Harrison|4.13|classicrock|The quiet Beatle’s triple album. “My Sweet Lord” and much more.
112|To Be Kind|Swans|4.06|drone|
113|The Lonesome Crowded West|Modest Mouse|4.10|indie|
114|Violator|Depeche Mode|4.06|postpunk|Synth-pop’s darkest hit record. The 1975 borrow a lot from it.
115|The Velvet Underground|The Velvet Underground|4.08|classicrock|
116|Hot Rats|Frank Zappa|4.08|prog|
117|Twin Fantasy (Face to Face)|Car Seat Headrest|4.03|indie|
118|Liquid Swords|GZA|4.10|goldrap|The coldest Wu-Tang solo record. RZA beats, chess metaphors.
119|Leaves Turn Inside You|Unwound|4.11|indie|90s post-hardcore turned dreamy. A lot of modern emo guitar tone is in here.
120|Ágætis byrjun|Sigur Rós|4.05|drone|
121|Future Days|Can|4.10|kraut|
122|Giant Steps|John Coltrane|4.12|jazz|
123|The Magnolia Electric Co.|Songs: Ohia|4.12|slowcore|
124|Music Has the Right to Children|Boards of Canada|4.03|electronic|
125|Post|Björk|4.01|pop|
126|My Favorite Things|John Coltrane|4.13|jazz|
127|Daydream Nation|Sonic Youth|4.03|indie|
128|The Infamous|Mobb Deep|4.12|goldrap|
129|The Bends|Radiohead|3.89|grunge|The guitar-heavy Radiohead. The easiest door into them for an emo fan.
130|Geogaddi|Boards of Canada|4.06|electronic|
131|A Moon Shaped Pool|Radiohead|3.96|indie|Late, gentle Radiohead with strings.
132|Spirit of Eden|Talk Talk|4.07|drone|
133|Tago Mago|Can|4.05|kraut|
134|Siamese Dream|The Smashing Pumpkins|4.02|grunge|
135|Blue|Joni Mitchell|4.07|folk|
136|Music for 18 Musicians|Steve Reich|4.11|classical|
137|Dopethrone|Electric Wizard|4.07|metal|
138|Flood|Boris|4.08|drone|
139|London Calling|The Clash|4.01|punk|
140|Songs for the Deaf|Queens of the Stone Age|4.02|grunge|Desert rock with Dave Grohl on drums.
141|Bringing It All Back Home|Bob Dylan|4.08|folk|
142|Swans Are Dead|Swans|4.31|drone|@live
143|Dirt|Alice in Chains|4.03|grunge|
144|Discipline|King Crimson|4.06|prog|
145|Untrue|Burial|4.00|electronic|
146|El jardín de los presentes|Invisible|4.12|argentina|
147|White Pony|Deftones|3.99|metal|
148|Fun House|The Stooges|4.06|punk|
149|Turn On the Bright Lights|Interpol|3.99|postpunk|NYC’s Joy Division revival. Moody and tight.
150|Ys|Joanna Newsom|4.05|folk|
151|Rust in Peace|Megadeth|4.03|metal|
152|Minecraft: Volume Alpha|C418|4.20|soundtrack|The Minecraft soundtrack. You’ve heard it whether you meant to or not.
153|The Powers That B|Death Grips|4.07|altrap|Jenny Death, the rock half of a double album. Death Grips with guitars.
154|Silent Hill 2|Akira Yamaoka|4.28|soundtrack|
155|Fôrça bruta|Jorge Ben|4.14|brazil|
156|Titanic Rising|Weyes Blood|4.01|indie|70s-style soft rock with a modern ache. A good one with the trop.
157|Boris at Last -Feedbacker-|Boris|4.05|drone|
158|Rage Against the Machine|Rage Against the Machine|4.00|metal|Rap-rock that still hits.
159|The Miseducation of Lauryn Hill|Lauryn Hill|4.04|rnb|
160|You Will Never Know Why|Sweet Trip|4.06|shoegaze|
161|The Dreaming|Kate Bush|4.06|pop|
162|Journey in Satchidananda|Alice Coltrane|4.10|spiritjazz|
163|White Light/White Heat|The Velvet Underground|4.01|classicrock|
164|Perfect From Now On|Built to Spill|4.07|indie|Long, spiraling guitar songs. Turnover-adjacent.
165|Meddle|Pink Floyd|3.98|prog|
166|After the Gold Rush|Neil Young|4.05|folk|
167|Uchu Nippon Setagaya|Fishmans|4.07|japan|
168|Mingus Ah Um|Charles Mingus|4.09|jazz|
169|Five Leaves Left|Nick Drake|4.05|folk|
170|Voodoo|D'Angelo|4.07|rnb|
171|Yeezus|Kanye West|3.86|kanye|
172|Hunky Dory|David Bowie|3.98|classicrock|
173|Larks' Tongues in Aspic|King Crimson|4.04|prog|
174|Black on Both Sides|Mos Def|4.08|goldrap|
175|ATLiens|OutKast|4.06|goldrap|OutKast’s spaced-out second album.
176|Alive 2007|Daft Punk|4.26|electronic|@live
177|On the Beach|Neil Young|4.08|folk|
178|Flower Boy|Tyler, The Creator|3.90|altrap|
179|LP!|JPEGMAFIA|3.99|altrap|
180|The Smile Sessions|The Beach Boys|4.25|classicrock|
181|"Heroes"|David Bowie|4.00|classicrock|
182|Rain Dogs|Tom Waits|4.03|folk|
183|Ready to Die|The Notorious B.I.G.|4.03|goldrap|
184|Modal Soul|Nujabes|4.04|jazz|
185|We Got It From Here... Thank You 4 Your Service|A Tribe Called Quest|4.05|goldrap|Tribe’s final album, and a great one.
186|Lateralus|Tool|3.99|metal|
187|Aja|Steely Dan|4.03|classicrock|
188|Head Hunters|Herbie Hancock|4.04|jazz|
189|Quebec|Ween|4.04|indie|Ween are from New Hope, PA, just up the river from Bristol.
190|Acabou chorare|Novos Baianos|4.10|brazil|
191|Jane Doe|Converge|4.02|metal|Metalcore’s masterpiece. Knocked Loose fans start here.
192|Dots and Loops|Stereolab|4.04|electronic|
193|Bocanada|Gustavo Cerati|4.08|argentina|
194|Odessey and Oracle|The Zombies|4.05|classicrock|
195|Get Up With It|Miles Davis|4.09|jazz|
196|Another Green World|Brian Eno|4.01|electronic|
197|Artaud|Pescado Rabioso|4.08|argentina|
198|Rust Never Sleeps|Neil Young|4.09|folk|
199|Construção|Chico Buarque|4.10|brazil|
200|Bottomless Pit|Death Grips|3.97|altrap|
201|Human|Death|4.05|deathmetal|
202|Fear of Music|Talking Heads|4.00|postpunk|
203|Painkiller|Judas Priest|4.05|metal|
204|Treasure|Cocteau Twins|4.01|shoegaze|
205|The Stone Roses|The Stone Roses|4.01|postpunk|
206|Purple Rain|Prince|4.14|soul|
207|Elliott Smith|Elliott Smith|4.04|slowcore|
208|Mount Eerie|The Microphones|4.04|slowcore|
209|None So Vile|Cryptopsy|4.05|deathmetal|
210|Expensive Shit|Fela Kuti|4.07|soul|
211|Townes Van Zandt|Townes Van Zandt|4.07|folk|
212|The Seer|Swans|4.01|drone|
213|MTV Unplugged in New York|Nirvana|4.17|grunge|@live
214|En el Palacio de Bellas Artes|Juan Gabriel|4.28|latin|@live
215|Funeral|Arcade Fire|3.92|indie|Huge, cathartic indie rock. Peak 2004.
216|Ram|Paul McCartney|4.05|classicrock|
217|Songs of Love and Hate|Leonard Cohen|4.05|folk|
218|Twin Peaks|Angelo Badalamenti|4.20|soundtrack|
219|Moanin'|Art Blakey and The Jazz Messengers|4.07|jazz|
220|Ege Bamyası|Can|4.01|kraut|
221|Speaking in Tongues|Talking Heads|4.00|postpunk|
222|Powerslave|Iron Maiden|4.02|metal|
223|Stratosphere|Duster|3.96|indie|
224|Demon Days|Gorillaz|3.90|pop|You know “Feel Good Inc.” The album’s better.
225|Scaring the Hoes|JPEGMAFIA & Danny Brown|3.90|altrap|You play Danny Brown a lot. This is him at his most chaotic.
226|Relationship of Command|At the Drive-In|4.01|posthc|Post-hardcore chaos. “One Armed Scissor” is the door.
227|A Tábua de Esmeralda|Jorge Ben|4.08|brazil|
228|Let My Children Hear Music|Charles Mingus|4.08|jazz|
229|The Velvet Rope|Janet Jackson|4.07|pop|
230|Magical Mystery Tour|The Beatles|4.08|classicrock|
231|Hellfire|black midi|3.94|prog|
232|Sound of Silver|LCD Soundsystem|3.96|electronic|Dance-punk with feelings. “All My Friends” is the one.
233|Dragon New Warm Mountain I Believe in You|Big Thief|3.99|indie|
234|Ghosts of the Great Highway|Sun Kil Moon|4.05|slowcore|
235|Third|Portishead|3.99|triphop|
236|Selling England by the Pound|Genesis|4.01|prog|
237|XO|Elliott Smith|4.02|slowcore|
238|Live at Red Rocks '22|King Gizzard & The Lizard Wizard|4.25|prog|@live
239|The New Sound|Geordie Greep|3.95|prog|
240|Reign in Blood|Slayer|3.98|metal|
241|Have One on Me|Joanna Newsom|4.05|folk|
242|A Crow Looked at Me|Mount Eerie|3.99|slowcore|A grief record, plainly sung. Heavy, but it stays with you.
243|Curtis|Curtis Mayfield|4.06|soul|
244|The Forever Story|JID|4.00|altrap|Atlanta rap with a J. Cole co-sign. Fast and dense.
245|First Utterance|Comus|4.03|prog|
246|Blue Train|John Coltrane|4.03|jazz|
247|The Mollusk|Ween|3.99|indie|More New Hope, PA weirdness, this time sea-themed.
248|Blackwater Park|Opeth|4.01|metal|
249|Everybody Knows This Is Nowhere|Neil Young|4.03|folk|
250|Kalk Samen Kuri no Hana|Sheena Ringo|4.04|japan|
251|Live Rope|Swans|4.25|drone|@live
252|Sign o' the Times|Prince|4.03|soul|
253|Kids See Ghosts|Kids See Ghosts|3.87|kanye|Kanye and Cudi as one. Twenty-four minutes.
254|Some Rap Songs|Earl Sweatshirt|3.91|altrap|
255|Yankee Hotel Foxtrot|Wilco|3.95|indie|
256|Sometimes I Might Be Introvert|Little Simz|3.97|altrap|
257|Getz/Gilberto|Stan Getz|4.01|brazil|
258|The Fragile|Nine Inch Nails|4.02|metal|
259|Repetition|Unwound|4.03|indie|
260|The Long Goodbye|LCD Soundsystem|4.25|electronic|@live
261|Maggot Brain|Funkadelic|3.99|soul|
262|Hejira|Joni Mitchell|4.05|folk|
263|The Olatunji Concert: The Last Live Recording|John Coltrane|4.23|jazz|@live
264|Weezer (Blue Album)|Weezer|3.87|grunge|You play Weezer. This is the one everyone loves.
265|Selected Ambient Works Volume II|Aphex Twin|3.96|electronic|
266|Sabbath Bloody Sabbath|Black Sabbath|3.99|metal|
267|Fresh Fruit for Rotting Vegetables|Dead Kennedys|3.98|punk|
268|Windswept Adan|Ichiko Aoba|4.00|japan|
269|Black Messiah|D'Angelo|4.02|rnb|
270|Zombie|Fela Kuti|4.05|soul|
271|Live at Carnegie Hall|Cameron Winter|4.22|indie|@live
272|Thick as a Brick|Jethro Tull|4.01|prog|
273|The Life of Pablo|Kanye West|3.83|kanye|
274|Pastel Blues|Nina Simone|4.04|soul|
275|The Fire This Time|Various Artists|4.06|soul|
276|Led Zeppelin|Led Zeppelin|3.92|classicrock|
277|Roseland NYC Live|Portishead|4.22|triphop|@live
278|If You're Feeling Sinister|Belle and Sebastian|3.97|indie|
279|The Glowing Man|Swans|4.00|drone|
280|Daughter of Darkness|Natural Snow Buildings|4.04|drone|
281|Drukqs|Aphex Twin|3.96|electronic|
282|Sticky Fingers|The Rolling Stones|3.98|classicrock|
283|Bryter Layter|Nick Drake|3.98|folk|
284|Heavy Metal|Cameron Winter|3.98|indie|Geese’s singer, solo. A 2024 RYM favorite.
285|Live in Chicago|Ween|4.26|indie|@live
286|Physical Graffiti|Led Zeppelin|3.97|classicrock|
287|Vaudeville Villain|Viktor Vaughn|4.00|altrap|DOOM under another alias. Sci-fi villain rap.
288|The Sound of Perseverance|Death|3.99|deathmetal|
289|The Name of This Band Is Talking Heads|Talking Heads|4.21|postpunk|@live
290|Mirage|Camel|4.01|prog|
291|Moment of Truth|Gang Starr|4.04|goldrap|
292|After the Night|Parannoul|4.21|shoegaze|Korean bedroom shoegaze that emo kids adopted. Very much your lane.
293|Graduation|Kanye West|3.82|kanye|
294|Raw Power|The Stooges|3.99|punk|
295|Brat|Charli xcx|3.82|pop|Charli’s big one. You play her a lot, so check it’s done front to back.
296|The Dance of the Moon and the Sun|Natural Snow Buildings|4.04|drone|
297|channel ORANGE|Frank Ocean|3.88|rnb|
298|Crooked Rain, Crooked Rain|Pavement|3.96|indie|
299|Cosmo's Factory|Creedence Clearwater Revival|4.01|classicrock|
300|Hot Buttered Soul|Isaac Hayes|4.03|soul|
301|Songs About Leaving|Carissa's Wierd|4.00|slowcore|
302|The Winter Ray|Natural Snow Buildings|4.06|drone|
303|Rock Dream|Boris with Merzbow|4.21|drone|@live
304|Symphony No. 9|Ludwig van Beethoven|4.07|classical|Karajan and the Berlin Phil. The “Ode to Joy” one.
305|0|Ichiko Aoba|4.01|japan|
306|Fragile|Yes|3.96|prog|
307|Vol. 4|Black Sabbath|3.97|metal|
308|Shouso Strip|Sheena Ringo|4.03|japan|
309|The Wall|Pink Floyd|3.83|prog|
310|Clics modernos|Charly García|4.04|argentina|
311|This Is Happening|LCD Soundsystem|3.94|electronic|
312|American Football|American Football|3.88|slowcore|
313|Ænima|Tool|3.94|metal|
314|Things Fall Apart|The Roots|4.00|goldrap|Philly’s own. Live-band rap at its peak.
315|Still Life|Opeth|4.00|metal|
316|Live at Massey Hall 1971|Neil Young|4.21|folk|@live
317|Off the Wall|Michael Jackson|3.96|soul|
318|Harvest|Neil Young|3.97|folk|
319|Blues & Roots|Charles Mingus|4.03|jazz|
320|Seventh Son of a Seventh Son|Iron Maiden|3.99|metal|
321|Die Mensch-Maschine|Kraftwerk|3.95|kraut|
322|From Mars to Sirius|Gojira|3.98|metal|
323|The Kinks Are the Village Green Preservation Society|The Kinks|3.99|classicrock|
324|New Plastic Ideas|Unwound|4.00|indie|
325|Plastic Beach|Gorillaz|3.88|pop|
326|Mellon Collie and the Infinite Sadness|The Smashing Pumpkins|3.92|grunge|
327|Kyuusai no Gihou|Susumu Hirasawa|4.02|japan|
328|The Ascension|Glenn Branca|3.97|drone|
329|Led Zeppelin II|Led Zeppelin|3.91|classicrock|
330|Pink|Boris|3.95|drone|
331|Promises|Floating Points|3.95|spiritjazz|
332|The Moon & Antarctica|Modest Mouse|3.96|indie|
333|Forever Changes|Love|3.95|classicrock|
334|UNDERTALE Soundtrack|Toby Fox|4.16|soundtrack|
335|Dark Magus|Miles Davis|4.19|jazz|@live
336|Love in Us All|Pharoah Sanders|4.04|spiritjazz|
337|Entertainment!|Gang of Four|3.95|postpunk|
338|Live at Revolution Hall|Adrianne Lenker|4.21|slowcore|@live
339|Crack the Skye|Mastodon|3.98|metal|
340|Wrong|NoMeansNo|4.00|punk|
341|Bridge Over Troubled Water|Simon & Garfunkel|3.97|folk|
342|Mama's Gun|Erykah Badu|4.00|rnb|
343|MTV Unplugged|Alice in Chains|4.17|grunge|@live
344|Absent Lovers: Live in Montreal 1984|King Crimson|4.21|prog|@live
345|Wild Is the Wind|Nina Simone|4.02|soul|
346|The Number of the Beast|Iron Maiden|3.94|metal|
347|Plastic Surgery Disasters|Dead Kennedys|3.99|punk|
348|Axis: Bold as Love|The Jimi Hendrix Experience|3.95|classicrock|
349|The Black Parade|My Chemical Romance|3.88|posthc|The scene-kid opera. You play MCR, so make sure this one’s done front to back.
350|Ascension|John Coltrane|3.99|jazz|
351|Storm of the Light's Bane|Dissection|3.98|deathmetal|
352|Stankonia|OutKast|3.93|goldrap|
353|Strange Days|The Doors|3.95|classicrock|
354|Ghost Reveries|Opeth|3.99|metal|
355|De todas las flores|Natalia Lafourcade|4.00|latin|
356|Foxtrot|Genesis|3.98|prog|
357|Mystic Stylez|Three 6 Mafia|3.98|goldrap|
358|By the Time I Get to Phoenix|Injury Reserve|3.90|altrap|
359|Welcome to Sky Valley|Kyuss|3.96|metal|
360|The Ape of Naples|Coil|3.96|electronic|
361|Juju|Siouxsie and the Banshees|3.97|postpunk|
362|Promise|Sade|4.00|rnb|
363|Grasa de las capitales|Serú Girán|4.03|argentina|
364|Mista Thug Isolation|Lil Ugly Mane|3.94|altrap|Memphis-style underground rap, a RYM cult favorite. Sits right next to Three 6 Mafia.
365|Nonagon Infinity|King Gizzard & The Lizard Wizard|3.93|prog|
366|Floating Into the Night|Julee Cruise|3.97|shoegaze|
367|The Great Deceiver: Live 1973-1974|King Crimson|4.20|prog|@live
368|The Great Annihilator|Swans|3.95|drone|
369|Minecraft: Volume Beta|C418|4.16|soundtrack|
370|The Bootleg Series Vol. 4: Live 1966|Bob Dylan|4.18|folk|@live
371|Performing "Flood"|Boris|4.19|drone|@live
372|You're Living All Over Me|Dinosaur Jr.|3.93|grunge|
373|Obscura|Gorguts|3.97|deathmetal|
374|Volcanic Bird Enemy and the Voiced Concern|Lil Ugly Mane|3.94|altrap|
375|Moving Pictures|Rush|3.93|prog|
376|Individual Thought Patterns|Death|3.97|deathmetal|
377|Exodus|Bob Marley & The Wailers|3.98|soul|
378|Pieces of a Man|Gil Scott-Heron|4.00|soul|
379|It Takes a Nation of Millions to Hold Us Back|Public Enemy|3.95|goldrap|
380|Born to Run|Bruce Springsteen|3.95|classicrock|
381|Close to a World Below|Immolation|4.00|deathmetal|
382|The Bootleg Series Vol. 5: Live 1975|Bob Dylan|4.19|folk|@live
383|Teens of Denial|Car Seat Headrest|3.92|indie|
384|Keep It Like a Secret|Built to Spill|3.96|indie|
385|Frances the Mute|The Mars Volta|3.94|posthc|At the Drive-In members gone full prog.
386|The Inner Mounting Flame|Mahavishnu Orchestra|3.98|jazz|
387|Blade Runner|Vangelis|4.15|soundtrack|
388|Películas|La Máquina de Hacer Pájaros|4.02|argentina|
389|Songs From the Big Chair|Tears for Fears|3.94|pop|“Everybody Wants to Rule the World” plus the rest of a great album.
390|Cheat Codes|Danger Mouse & Black Thought|3.95|goldrap|The Roots’ Black Thought over Danger Mouse beats. Philly bars.
391|At the Mountains of Madness|Electric Masada|4.18|jazz|@live
392|Hammersmith Odeon, London '75|Bruce Springsteen|4.19|classicrock|@live
393|Koi No Yokan|Deftones|3.93|metal|
394|Deceit|This Heat|3.93|postpunk|
395|Aethiopes|billy woods|3.95|altrap|
396|Lanquidity|Sun Ra|3.99|spiritjazz|
397|Africa/Brass|John Coltrane|4.00|jazz|
398|Three Cheers for Sweet Revenge|My Chemical Romance|3.90|posthc|
399|Javelin|Sufjan Stevens|3.94|indie|
400|Vision Creation Newsun|Boredoms|3.96|japan|
"""
LIVE='A live album RYM rates above most studio records.'
for line in L.strip().split("\n"):
    a=line.split("|")
    lane,anc,blurb=CL[a[4]]
    why=a[5] if len(a)>5 and a[5] else ''
    why= (blurb+' '+LIVE) if why=='@live' else (why or blurb)
    RYM.append(dict(rank=int(a[0]),rating=float(a[3]),artist=a[2],album=a[1],year='',lane=lane,canon=False,anchors=anc,why=why,alts=''))
