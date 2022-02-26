import pysheds
import pytest

from flows_n_snows import watershed


def test_retrieve_dem_and_grid():
    grid, dem = watershed.retrieve_dem_and_grid()  # add smaller dataset for testing
    assert type(grid) == pysheds.sgrid.sGrid
    assert type(dem) == pysheds.sview.Raster
