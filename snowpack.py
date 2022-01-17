
import ulmo
import pandas as pd
import numpy as np
import matplotlib
from datetime import datetime

WSDL_URL = 'https://hydroportal.cuahsi.org/Snotel/cuahsi_1_1.asmx?WSDL'

# site_info = ulmo.cuahsi.wof.get_site_info(WSDL_URL, 'SNOTEL:452_UT_SNTL')

SITE = 'SNOTEL:452_UT_SNTL'
SNOW_WATER_EQUIV = 'SNOTEL:WTEQ_D'

def fetch_snotel_to_df():
    snow_data = ulmo.cuahsi.wof.get_values(WSDL_URL, SITE, SNOW_WATER_EQUIV, start='1980-01-01', end=datetime.today().strftime('%Y-%m-%d'))

    values_df = pd.DataFrame.from_dict(snow_data['values'])
    values_df['datetime'] = pd.to_datetime(values_df['datetime'], utc=True)
    values_df = values_df.set_index('datetime')
    values_df['value'] = pd.to_numeric(values_df['value']).replace(-9999, np.nan)
    values_df = values_df[values_df['quality_control_level_code'] == '1']

    return values_df

def fetch_flows_to_df():
    flow_data = ulmo.usgs.nwis.get_site_data('09337500', service='daily', start='1980-01-01', end=datetime.today().strftime('%Y-%m-%d'))
    flow_data = flow_data['00060:00003']['values']
    values_df = pd.DataFrame.from_dict(flow_data)

    return values_df

print(fetch_flows_to_df().head())