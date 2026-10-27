import pandas as pd, numpy as np
df=pd.read_pickle('df.pkl')
df['y']=df.ts.dt.year; df['m']=df.ts.dt.month; df['dow']=df.ts.dt.dayofweek; df['h']=df.ts.dt.hour
df['d']=df.ts.dt.tz_localize(None).dt.normalize()
T=lambda s: pd.Timestamp(s,tz='America/New_York')
CH=[('High school','2011-07-01','2015-08-31','Bus rides, blog rap and the scene kid years'),
('College','2015-08-31','2019-06-01','Pregames, pop-punk and the SoundCloud takeover'),
('After college','2019-06-01','2019-10-28','Between graduation and the first city job'),
('NYC office','2019-10-28','2020-03-16','Commuting into Minute Media in the city'),
('COVID at home','2020-03-16','2020-09-01','Lockdown'),
('Bloomfield, NJ','2020-09-01','2021-09-01','First place after lockdown'),
('Philly','2021-09-01','2024-09-01','Three years in Philadelphia'),
('Bristol with Katie','2024-09-01','2026-09-14','Moving in together, engaged in Nov 2024, married Aug 2026'),
('Glenmede','2026-09-14','2100-01-01','Married, settled in Bristol, and a new job at Glenmede: the right-now era')]
def chap(ts):
    for n,a,b,_ in CH:
        if T(a)<=ts<T(b): return n
df['chapter']=pd.cut(df.uts,[T(a).timestamp() for _,a,_,_ in CH]+[T(CH[-1][2]).timestamp()],labels=[c[0] for c in CH],right=False).astype(str)
