import pandas as pd
import numpy as np

'''
This function interpolates the AIS data. The function interpolates and resamples into every 3 minutes.
The interpolation occurs only if the time gaps between two points is less than 15 minutes. 
'''


def interpolate_aisData(aisDataFileName):
    df = pd.read_csv(aisDataFileName)

    df['Gaps(Hrs)'] = np.where(df['mmsi'] == df['mmsi'].shift(-1),
                               ((abs(df['timestamp'] - df['timestamp'].shift(-1))) / (1000 * 60 * 60)),
                               np.nan_to_num(0)
                               )

    df = df.set_index(['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')
    '''
    Interpolation continues if gaps is less than 15 minutes between two location. If there is more than 15 mins gap
    then interpolation skips those points
    and again continue from the next data points.
    '''

    df.loc[(df['mmsi'] != df['mmsi'].shift()) | (df['Gaps(Hrs)'].shift() > 0.25), 'Temp_MMSI'] = 1

    df['Temp_MMSI'] = df['Temp_MMSI'].cumsum().ffill()

    df1 = (df.groupby('Temp_MMSI', axis=0)
           [['mmsi', 'latitude', 'longitude']]
           .resample('3min')
           .mean()
           .groupby(level=0)
           .apply(lambda x: x.interpolate(method='linear')).reset_index().drop('Temp_MMSI', 1))

    df1['mmsi'] = df1['mmsi'].astype(int)

    df1.set_index(('mmsi'), inplace=True)

    df1[['latitude', 'longitude']] = df1[['latitude', 'longitude']]\
        .apply(lambda x: pd.Series.round(x, 4))

    df1.to_csv('InterpolatedAISData.csv')