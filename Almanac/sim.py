import pandas as pd, collections, bisect
df=pd.read_pickle('df.pkl')
base=pd.Timestamp('2025-12-09 21:16:08',tz='UTC')
pre=df[df.dt<base]; post=df[df.dt>=base]
cnt=collections.Counter(pre.artist)
# order for ties: earliest reaching -> use last uts
lastreach={a:t for a,t in pre.groupby('artist').uts.max().items()}
def top(cnt,lastreach,N=500):
    return sorted(cnt,key=lambda a:(-cnt[a],lastreach[a]))[:N]
t0=set(top(cnt,lastreach))
freq=collections.Counter(cnt.values())
keys=sorted(freq)  # ascending
inset=set(t0); entries=collections.defaultdict(list); exits=collections.defaultdict(list)
events=[]
for r in post.itertuples():
    a=r.artist; old=cnt[a]
    if old: 
        freq[old]-=1
    cnt[a]=old+1; freq[old+1]+=1; lastreach[a]=r.uts
    c=old+1
    rank=sum(v for k,v in freq.items() if k>=c)
    if rank<=500 and a not in inset:
        inset.add(a); entries[a].append((r.dt,rank,c))
        # someone got bumped: the one at rank 501
        if len(inset)>500:
            # find lowest in inset
            low=min(inset,key=lambda x:(cnt[x],-lastreach[x]))
            inset.remove(low); exits[low].append((r.dt,c,a))
final=set(top(cnt,lastreach))
print(len(inset), len(final&inset))
ever=[a for a in entries if a not in t0]
print('ever entered',len(ever))
rows=[]
for a in ever:
    rows.append(dict(artist=a,first_entry=entries[a][0][0],entries=len(entries[a]),exits=len(exits.get(a,[])),in_now=a in final,base=pre.artist.value_counts().get(a,0),now=cnt[a]))
r=pd.DataFrame(rows).sort_values('first_entry')
pd.set_option('display.width',200)
print(r.to_string())
fell=[a for a in t0 if a not in final]
print('fell',len(fell))
