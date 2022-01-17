import pandas as pd
import dataretrieval.nwis as nwis

site = '09337500'

df = nwis.get_record(sites=site, service='dv', start='2021-05-01', end='2021-05-01',parameterCd='00060')


df = df[(df['00060_Mean']> -999999.0) & (df['00060_Mean']< 100)]
df['dt'] = df.index
