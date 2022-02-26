from typing import Optional

import xarray as xr
from pysheds.grid import Grid


def retrieve_dem_and_grid(
    dem_path: Optional[str] = "../data/srtm1_90m_utah.tif",
) -> tuple:
    """Retrieves grid and dem for pysheds watershed basin delineation.
    TODO: add subsetting based on bbox

    Parameters
    ----------
    dem_path : Optional[str], optional
        data path, by default '../data/srtm1_90m_utah.tif'

    Returns
    -------
    tuple
        tuple containing grid and dem
    """
    # ds = xr.open_dataset(srtm_path, engine="rasterio")
    grid = Grid.from_raster(dem_path)
    dem = grid.read_raster(dem_path)
    return (grid, dem)


def fill_depressions(grid, dem):
    return grid.fill_depressions(dem)


def resolve_flats(grid, dem):
    return grid.resolve_flats(dem)


def calc_flow_dir(grid, dem):
    return grid.flowdir(dem)


def calculate_catchment_basin(grid, flowdir, pp_lat: float, pp_lon: float):

    catch = grid.catchment(x=pp_lon, y=pp_lat, fdir=flowdir, xytype="coordinate")
    return catch


def clip_catchment_to_grid(grid, catch):
    clipped_catch = grid.clip_to(catch)
    return clipped_catch


# TODO:
# catchment area to geopandas?
