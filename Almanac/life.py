import pandas as pd, numpy as np
df=pd.read_pickle('df.pkl')
df['y']=df.ts.dt.year; df['m']=df.ts.dt.month; df['dow']=df.ts.dt.dayofweek; df['h']=df.ts.dt.hour
df['d']=df.ts.dt.tz_localize(None).dt.normalize()
T=lambda s: pd.Timestamp(s,tz='America/New_York')
# Life chapters are where Capy lived. Work and school are separate (PER in life_build.py).
CH=[('Milltown, NJ','2011-07-01','2015-08-31','Home through high school: bus rides, blog rap and the scene kid years'),
('Poughkeepsie, NY','2015-08-31','2019-05-25','Marist: pregames, pop-punk and the SoundCloud takeover'),
('Milltown, NJ (again)','2019-05-25','2020-09-01','Back home after Marist: the NYC commute to Minute Media, then lockdown'),
('Bloomfield, NJ','2020-09-01','2021-09-01','First place after lockdown'),
('Philly','2021-09-01','2024-09-01','Three years in Philadelphia'),
('Bristol','2024-09-01','2100-01-01','With Katie: moved in Sep 2024, engaged Nov 2024, married Aug 2026')]
def chap(ts):
    for n,a,b,_ in CH:
        if T(a)<=ts<T(b): return n
df['chapter']=pd.cut(df.uts,[T(a).timestamp() for _,a,_,_ in CH]+[T(CH[-1][2]).timestamp()],labels=[c[0] for c in CH],right=False).astype(str)
