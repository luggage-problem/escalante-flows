import pandas as pd
import ulmo

site = '09337500'

df = ulmo.usgs.nwis.get_site_data(site_code = site)