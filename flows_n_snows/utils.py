import ulmo
import pandas as pd
import numpy as np
import matplotlib
from datetime import datetime
import pdb
import re

def get_all_snotel_sites():
    #   ntwk, state, site_name, ts, start, lat, lon, elev, county, huc, site_id
    SNOTEL_LIST_URL = "https://wcc.sc.egov.usda.gov/nwcc/yearcount?network=sntl&state=&counttype=statelist"
    table = pd.read_html(SNOTEL_LIST_URL)[1]
    table['site_id'] = 'SNOTEL:' + re.findall('\((.*?)\)', str(table['site_name']))[0] + '_' + table['state'] + '_SNTL'
    return table


def fetch_snotel_to_df(site_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    WSDL_URL = "https://hydroportal.cuahsi.org/Snotel/cuahsi_1_1.asmx?WSDL"
    SNOW_WATER_EQUIV = "SNOTEL:WTEQ_D"
    snow_data = ulmo.cuahsi.wof.get_values(
        WSDL_URL,
        site_id,
        SNOW_WATER_EQUIV,
        start=start_date,
        end=end_date,
    )

    values_df = pd.DataFrame.from_dict(snow_data["values"])
    values_df["datetime"] = pd.to_datetime(values_df["datetime"], utc=True)
    values_df = values_df.set_index("datetime")
    values_df["value"] = pd.to_numeric(values_df["value"]).replace(-9999, np.nan)
    values_df = values_df[values_df["quality_control_level_code"] == "1"]

    return values_df


def fetch_flows_to_df(
    river_id: str,
    start_date: str,
    end_date: str,
    interval: str = "daily",
    estimation_drop: bool = False,
) -> pd.DataFrame:
    flow_data = ulmo.usgs.nwis.get_site_data(
        river_id,
        service=interval,
        start=start_date,
        end=end_date,
    )
    flow_data = flow_data["00060:00003"]["values"] # 00060:00003 is flow data identifier (probably)
    values_df = pd.DataFrame.from_dict(flow_data) # todo: handle replacing null values and such
    values_df["datetime"] = pd.to_datetime(values_df["datetime"], utc=True)
    values_df["value"] = values_df["value"].astype(float)

    if estimation_drop == True:
        # Data-value qualification codes included in this output:
        #     A  Approved for publication -- Processing and review completed.
        #     P  Provisional data subject to revision.
        #     e  Value has been estimated.
        values_df["value"] = values_df[values_df["qualifiers"] == "A"]
    values_df = values_df.set_index("datetime")
    return values_df

