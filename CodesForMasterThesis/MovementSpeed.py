import pandas as pd
from haversine import haversine
import numpy as np

'''
This function calculates the speed as mentioned in the thesis. 
'''


def calculateSpeed(aisDataFileNameFromMeasurementArea):
    result = pd.read_csv(aisDataFileNameFromMeasurementArea)

    result['Lats'] = result['latitude'].shift(-1)
    result['Lons'] = result['longitude'].shift(-1)

    result['Lats1'] = result['latitude'].shift(1)
    result['Lons1'] = result['longitude'].shift(1)

    result['Distance'] = \
        np.where(((result['mmsi'] == result['mmsi'].shift(-1)) & (result['Gaps(hrs)'] < 4)),
                 abs(result.apply(lambda x: haversine((x['Lats1'], x['Lons1']), (x['Lats'], x['Lons'])),
                                  axis=1)), np.nan)

    result.drop(['Lats', 'Lons', 'Lats1', 'Lons1'], axis=1, inplace=True)
    result.dropna(inplace=True)

    result['speedTime'] = np.where(((result['mmsi'] == result['mmsi'].shift(-1)) & (result['Gaps(hrs)'] < 4)),
                                   (result['timestamp'].shift(-1) - result['timestamp'].shift(1)),
                                   np.nan)

    result.dropna(inplace=True)

    result['speed'] = np.where(((result['mmsi'] == result['mmsi'].shift(-1))),
                               (result['Distance'] * 1000) / result['speedTime'], np.nan)

    result.dropna(inplace=True)

    result.drop(['speedTime', 'Distance'], axis=1, inplace=True)

    result['speed'] = result['speed'].round(3)
    result['latitude'] = result['latitude'].round(3)
    result['Gaps(hrs)'] = result['Gaps(hrs)'].round(3)
    result['longitude'] = result['longitude'].round(3)

    result.to_csv('AISDataWithSpeed.csv', index=0)
