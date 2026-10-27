# "Sounds like": Capy's own sense of who is close to whom, from the categorizing game (my_categorize.json,
# pulled from the artifact before each refresh). Three kinds of link: sound (they sound alike), scene (same crew,
# tours or features), member (a group and someone in it). Also scores each answer against the galaxy's co-listening pick.
import json, os, re, pandas as pd
if not os.path.exists('my_categorize.json'):
    pd.DataFrame(columns=['anchor', 'artist', 'kind', 'how']).to_csv('out/sounds_like.csv', index=False)
    pd.DataFrame(columns=['anchor', 'your_pick', 'galaxy_pick', 'verdict']).to_csv('out/sounds_scorecard.csv', index=False); raise SystemExit
A = [x for x in json.load(open('my_categorize.json'))['answers'] if x.get('q') in ('closer_to', 'closest')]
# links that are about people rather than sound, from Capy's notes
KIND = {('BabyTron', 'ShittyBoyz'): 'member', ('Heems', 'Das Racist'): 'member', ('oso oso', 'Prince Daddy & The Hyena'): 'scene',
        ('Famous Dex', 'Rich the Kid'): 'scene', ('Famous Dex', 'Jay Critch'): 'scene', ('Donnie Trumpet & The Social Experiment', 'Chance the Rapper'): 'scene',
        ('Donnie Trumpet & The Social Experiment', 'Snakehips'): 'scene'}
EXTRA = [('oso oso', 'Prince Daddy & The Hyena', 'scene', 'your note'), ('Famous Dex', 'Jay Critch', 'scene', 'your note'),
         ('Donnie Trumpet & The Social Experiment', 'Chance the Rapper', 'scene', 'your note'), ('Donnie Trumpet & The Social Experiment', 'Snakehips', 'scene', 'your note')]
def names(s):
    s = re.sub(r'^Neither:\s*', '', s); s = re.sub(r'\balso\b', '', s)
    return [n.strip() for n in re.split(r',| and ', s) if n.strip()]
E = pd.read_csv('out/solar_edges.csv'); J = {}
for a, b, j in E[['source', 'target', 'jaccard']].itertuples(index=False): J[frozenset((a, b))] = max(j, J.get(frozenset((a, b)), 0))
rows, score = [], []
for x in A:
    an, pk, gal = x['anchor'], x['pick'], x.get('galaxy')
    if pk.startswith("Don't"): continue
    if x['q'] == 'closest':
        picks, how = ['MUNA', 'Phoebe Bridgers'], 'your pick'
    elif pk == 'Both':
        picks, how = [x['a'], x['b']], 'both close'
    elif pk.startswith('All three'):
        picks, how = [x['a'], x['b']], 'all close'
    elif pk.startswith('Neither'):
        picks, how = names(pk) if ':' in pk else [], 'write-in'
    elif 'orbit' in pk:
        picks, how = [], ''
    else:
        picks, how = [pk], 'your pick'
    for p in picks: rows.append((an, p, KIND.get((an, p), 'sound'), how))
    if gal is None and x['q'] == 'closer_to':   # early rounds: the galaxy's pick is whichever of the two it links more strongly
        ja, jb = J.get(frozenset((an, x['a'])), 0), J.get(frozenset((an, x['b'])), 0)
        gal = x['a'] if ja > jb else x['b'] if jb > ja else None
    verdict = 'agree' if gal and (pk == gal or pk == 'Both' or pk.startswith('All three')) else ('differ' if gal else '')
    score.append((an, pk, gal or '', verdict))
rows += EXTRA
# direct links Capy gave while tagging (q = link): kind is set by him
for x in json.load(open('my_categorize.json'))['answers']:
    if x.get('q') == 'link': rows.append((x['anchor'], x['artist'], x.get('kind', 'sound'), 'your note'))
S = pd.DataFrame(rows, columns=['anchor', 'artist', 'kind', 'how']).drop_duplicates(['anchor', 'artist'])
S.to_csv('out/sounds_like.csv', index=False)
pd.DataFrame(score, columns=['anchor', 'your_pick', 'galaxy_pick', 'verdict']).to_csv('out/sounds_scorecard.csv', index=False)
print('sounds_like', len(S), S.kind.value_counts().to_dict())
