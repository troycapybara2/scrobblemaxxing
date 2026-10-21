import pandas as pd, json, os
O='out/'
k=pd.read_csv(O+'kpis.csv')
rf=pd.read_csv(O+'race_facts.csv'); ex=json.load(open(O+'extra.json'))
lab={'hoodie_plays':'Hoodie Allen plays','uzi_plays':'Lil Uzi Vert plays','gap':'Plays separating them','uzi_per_month':'Uzi plays per month (blended pace)','hoodie_per_month':'Hoodie plays per month (blended pace)','eta_mid':'Projected takeover date','eta_fast':'Takeover date at 90-day pace','eta_slow':'Takeover date at 365-day pace','hoodie_years_at_1':'Year-ends Hoodie Allen has finished #1','uzi_first':'First Lil Uzi Vert scrobble','hoodie_last_play':'Last Hoodie Allen scrobble'}
rf['label']=rf.metric.map(lab)
k=k[k.metric!='hoodie_uzi_gap']
extra=pd.DataFrame([('longest_streak_days',ex['streak']['size'],'Longest run of consecutive days with a scrobble'),
 ('streak_start',ex['streak']['min'][:10],'Streak start'),('streak_end',ex['streak']['max'][:10],'Streak end'),
 ('app_snapshots',ex['app_snapshots'],'Leaderboard snapshots the app saved'),('app_last',ex['app_last'][:10],'Last app snapshot')],columns=['metric','value','label'])
pd.concat([k,rf,extra]).to_csv(O+'kpis.csv',index=False)
for f in ['top_albums','top_tracks','repeat_days']:
    d=pd.read_csv(O+f+'.csv'); d.drop(columns=[c for c in ['key'] if c in d]).to_csv(O+f+'.csv',index=False)
fix={}
for f in ['top500_entrants','top500_now','projection_entrants']:
    d=pd.read_csv(O+f+'.csv',dtype=str,keep_default_na=False)
    for a,s in fix.items(): d.loc[d.artist==a,'scene']=s
    d.to_csv(O+f+'.csv',index=False)
os.remove(O+'race_facts.csv'); os.remove(O+'extra.json')
for f in os.listdir(O):
    if '—' in open(O+f).read(): print('emdash',f)
