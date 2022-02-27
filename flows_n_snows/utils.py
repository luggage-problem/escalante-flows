import re

import flows_n_snows.config
import numpy as np
import pandas as pd
import ulmo
import xarray as xr



def get_all_snotel_sites() -> pd.DataFrame:
    """Return dataframe containing all snotel site ids
    Header is: ntwk, state, site_name, ts, start, lat, lon, elev, county, huc, site_id


    Returns
    -------
    Pandas DataFrame
        Dataframe containing snotel site ids
    """
    SNOTEL_LIST_URL = (
        "https://wcc.sc.egov.usda.gov/nwcc/yearcount?network=sntl&state=&counttype=statelist"
    )
    table = pd.read_html(SNOTEL_LIST_URL)[1]
    table_state = table["state"]
    site_name = re.findall(r"\((.*?)\)", str(table["site_name"]))[0]  # noqa W605
    table["site_id"] = f"SNOTEL:{site_name}_{table_state}_SNTL"
    return table


def fetch_snotel_to_df(site_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Returns dataframe containing snotel data from input site_id for date range.

    Parameters
    ----------
    site_id : str
        snotel site id
    start_date : str
       start date bounds
    end_date : str
        end date bounds

    Returns
    -------
    pd.DataFrame
        DataFrame containing snotel site data for SWE
    """
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
    values_df["datetime"] = pd.to_datetime(values_df["datetime"]).dt.strftime("%Y-%m-%d:%H:%M:%S")
    values_df = values_df.set_index("datetime")
    values_df["value"] = pd.to_numeric(values_df["value"]).replace(-9999, np.nan)
    values_df = values_df[values_df["quality_control_level_code"] == "1"]

    return values_df


def fetch_flows_to_df(
    gauge_id: str,
    start_date: str,
    end_date: str,
    interval: str = "daily",
    estimation_drop: bool = False,
) -> pd.DataFrame:
    """Fetch river flow from input gauge ID

    Parameters
    ----------
    gauge_id : str
        USGS stream gauge ID
    start_date : str
        Start date bounds. ex. 2000-01-01
    end_date : str
        End date bounds. ex. 2000-01-01
    interval : str, optional
        site collection interval by default "daily"
    estimation_drop : bool, optional
        Bool to include for remove gauge data that has been estimated --  by default False

    Returns
    -------
    pd.DataFrame
        _description_
    """
    flow_data = ulmo.usgs.nwis.get_site_data(
        gauge_id,
        service=interval,
        start=start_date,
        end=end_date,
    )
    # 00060:00003 is flow data identifier (probably)
    flow_data = flow_data["00060:00003"]["values"]
    # todo: handle replacing null values and such
    values_df = pd.DataFrame.from_dict(flow_data)
    # rename
    # import pdb
    # pdb.set_trace()
    values_df = values_df.rename({"value": "flow_rate", "qualifiers": "flags"}, axis='columns')
    values_df["datetime"] = pd.to_datetime(values_df["datetime"]).dt.strftime("%Y-%m-%d:%H:%M:%S")
    values_df["flow_rate"] = values_df["flow_rate"].astype(float)

    if estimation_drop is True:
        # Data-value qualification codes included in this output:
        #     A  Approved for publication -- Processing and review completed.
        #     P  Provisional data subject to revision.
        #     e  Value has been estimated.
        values_df["flow_rate"] = values_df[values_df["flags"] == "A"]
    values_df = values_df.set_index("datetime")
    return values_df


def query_zarr_dates(path: str) -> slice:
    xdf = read_zarr_store(path)
    min_date = xdf.datetime.min()
    max_date = xdf.datetime.max()
    return slice(min_date, max_date)


def dataframe_to_xarray(df: pd.DataFrame) -> xr.Dataset:
    return df.to_xarray()


def dataframe_to_zarr(df: pd.DataFrame, path: str, mode: str = 'w-', append_dim=None):
    ds = dataframe_to_xarray(df)
    ds.to_zarr(path, consolidated=True, mode=mode, append_dim=append_dim)


def read_zarr_store(path):
    return xr.open_zarr(path, consolidated=True)


# def append_to_zarr_store(path: str, xdf: xr.Dataset):


# df = fetch_flows_to_df(config.river_gauge, start_date="1900-01-01", end_date="2023-01-01")
# # df2 = fetch_flows_to_df(config.river_gauge, start_date="2000-01-02", end_date="2000-01-02")

# path = './flow_zarr.zarr'
# dataframe_to_zarr(df, path)
# dataframe_to_zarr(df2, path, mode='a', append_dim='datetime')

# xdf = read_zarr_store(path)
