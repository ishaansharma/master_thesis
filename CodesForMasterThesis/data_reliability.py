import pandas as pd
import numpy as np
from haversine import haversine

''''
Checks some AIS reliability issues shown in the thesis. 
'''


def loadAISData(aisDataFileName):
    result = pd.read_csv(aisDataFileName)

    result['Lats'] = result['latitude'].shift(-1)
    result['Lons'] = result['longitude'].shift(-1)

    result['Consecutive Distance(KM)'] = \
        np.where(result['mmsi'] == result['mmsi'].shift(-1),
                 abs(result.apply(lambda x: haversine((x['latitude'], x['longitude']), (x['Lats'], x['Lons'])),
                                  axis=1)), np.nan_to_num(0))

    result = result.loc[(result['Consecutive Distance(KM)'] > 10) & (result['mmsi'] == 244224000)]

    result['timestamp'] = pd.DatetimeIndex(result['timestamp'])
    result.drop(['Lats', 'Lons'], axis=1, inplace=True)
    result.set_index('timestamp', inplace=True)

    result = result.loc['2019-06-12 9:42:00':'2019-06-12 18:42:00']

    result = result.loc[(result['mmsi'] == 244224000)]

    print(result.to_csv('HighConsecutiveGaps.csv'))
