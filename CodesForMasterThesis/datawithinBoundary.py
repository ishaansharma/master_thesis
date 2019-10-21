from CreatingMeasurementArea import GenerateMeasurementBoundary
import pandas as pd
import numpy as np

'''
this function loads the main AIS data file and filters the AIS data that are part of the measurement area
'''


def filterDataForMeasurementArea(interpolatedAISdataFileName):
    df = pd.read_csv(interpolatedAISdataFileName)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].values.astype(np.int64) // 10 ** 9

    df['Gaps(hrs)'] = np.where(df['mmsi'] == df['mmsi'].shift(-1),
                               ((abs(df['timestamp'] - df['timestamp'].shift(-1))) / 3600), np.nan_to_num(0)
                               )

    df['IsWithin'] = df.apply(lambda x: GenerateMeasurementBoundary(x['longitude'], x['latitude']), axis=1)

    df.dropna(how='any', axis=0, inplace=True)

    df.drop(['IsWithin', 'Gaps(hrs)'], axis=1, inplace=True)

    df['Gaps(hrs)'] = np.where(df['mmsi'] == df['mmsi'].shift(-1),
                               ((abs(df['timestamp'] - df['timestamp'].shift(-1))) / 3600), np.nan_to_num(0)
                               )
    df[['latitude', 'longitude', 'Gaps(hrs)']] = df[['latitude', 'longitude', 'Gaps(hrs)']].apply(
        lambda x: pd.Series.round(x, 3))
    df.to_csv('BoundaryAISData.csv', index=0)
