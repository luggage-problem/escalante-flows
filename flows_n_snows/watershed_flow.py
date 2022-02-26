from prefect import Flow, task

from flows_n_snows.watershed import (
    calc_flow_dir,
    calculate_catchment_basin,
    clip_catchment_to_grid,
    fill_depressions,
    resolve_flats,
    retrieve_dem_and_grid,
)

dem_grid_task = task(retrieve_dem_and_grid, nout=2)
fill_depression_task = task(fill_depressions)
resolve_flats_task = task(resolve_flats)
flow_dir_task = task(calc_flow_dir)
calculate_catchment_basin_task = task(calculate_catchment_basin)
clip_catchment_to_grid_task = task(clip_catchment_to_grid)

pp_lat = 37.778
pp_lon = -111.575
with Flow(name="catchment") as flow:
    grid, dem = dem_grid_task
    filled_depressions = fill_depression_task(grid, dem)
    resolved_flats = resolve_flats_task(grid, filled_depressions)
    flow_dir = flow_dir_task(grid, resolved_flats)
    catch_basin = calculate_catchment_basin_task(grid, flow_dir, pp_lat, pp_lon)
    clipped_catch = clip_catchment_to_grid_task(grid, catch_basin)
