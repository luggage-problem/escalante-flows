from typing import Optional

import pysheds
import os
from pysheds.grid import Grid
import xarray as xr


def retrieve_dem_and_grid(
    dem_path: Optional[str] = "../data/srtm1_30m_utah.tif",
) -> tuple:
    """Retrieves grid and dem for pysheds watershed basin delineation.
    TODO: add subsetting based on bbox

    Parameters
    ----------
    dem_path : Optional[str], optional
        data path, by default '../data/srtm1_30m_utah.tif'

    Returns
    -------
    tuple
        tuple containing grid and dem
    """
    # ds = xr.open_dataset(srtm_path, engine="rasterio")
    grid = Grid.from_raster(dem_path)
    dem = grid.read_raster(dem_path)
    return (grid, dem)
