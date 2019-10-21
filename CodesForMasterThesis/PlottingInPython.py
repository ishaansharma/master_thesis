import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib.patches as mpatches

os.environ["PROJ_LIB"] = "F:\\AllExternalSoftwares\\conda\\envs\\venv\\Library\\share";  # fixr
from mpl_toolkits.basemap import Basemap

''''
This functions does the general plotting of different data at different stages. The was modified many times according
to the necessary of the plotting. The sample code is below. 
'''

df = pd.read_csv('InterpolatedAISData.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp'] = df['timestamp'].values.astype(np.int64) // 10 ** 9

df['Gaps(hrs)'] = np.where(df['mmsi'] == df['mmsi'].shift(-1),
                           ((abs(df['timestamp'] - df['timestamp'].shift(-1))) / ( 60 * 60)),
                           np.nan_to_num(0)
                           )

colors = np.where(((df['Gaps(hrs)'] > 1) & (df['Gaps(hrs)'] < 6)), 'r', 'g')

lat = df['latitude'].values
lon = df['longitude'].values

lat_margin = 0.75
lon_margin = 0.75
lat_min = min(lat) - lat_margin
lat_max = max(lat) + lat_margin
lon_min = min(lon) - lon_margin
lon_max = max(lon) + lon_margin

m = Basemap(llcrnrlon=lon_min,
            llcrnrlat=lat_min,
            urcrnrlon=lon_max,
            urcrnrlat=lat_max,
            lat_0=(lat_max - lat_min) / 2,
            lon_0=(lon_max - lon_min) / 2,
            projection='merc',
            resolution='h',
            area_thresh=10,
            )

m.drawcoastlines()

m.drawstates()
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='white', lake_color='#85A6D9')
lons, lats = m(lon, lat)


m.scatter(lons, lats, zorder=5, c= colors, s = 10)
plt.title('Some title', fontsize=12)

low = mpatches.Patch(color='green', label='Data gaps < 1 hr')
med = mpatches.Patch(color='red', label='Data gaps > 1 hr')

plt.legend(handles=[low, med], title= 'Information of data gaps')

plt.savefig('MainFigure.png')