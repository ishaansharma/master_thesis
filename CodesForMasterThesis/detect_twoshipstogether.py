import pandas as pd
import numpy as np
from haversine import haversine
from scipy.spatial.distance import cdist

'''
This is sample code and the function was edited many times according to the requirements. The function 
finds the encounter if exists. The function also returns file that contains information such as encounter date time,
closet distance, etc. 
'''


def find_encounters(AISDataWithCloseToZeroSpeed, enounterShip1Mmsi, encounterShip2Mmsi):
    df = pd.read_csv(AISDataWithCloseToZeroSpeed)

    # delete the unnecessary columns
    df.drop(['Gaps(hrs)', 'speed'], axis=1, inplace=True)

    # this is one of the encounter ship's data
    target = df.loc[df['mmsi'] == enounterShip1Mmsi]

    target.reset_index(drop=True, inplace=True)

    # this is another ship's encounter data
    outsider1 = df.loc[df['mmsi'] == encounterShip2Mmsi]
    outsider1.reset_index(drop=True, inplace=True)

    home_latlon = target[['latitude', 'longitude']]
    outsider1_latlon = outsider1[['latitude', 'longitude']]

    outsider1_timestamp = outsider1[['timestamp']]

    distanceCalc = cdist(home_latlon, outsider1_latlon, metric=haversine)

    numbers_columns = len(outsider1.index)
    result_calc = pd.DataFrame(distanceCalc, columns=np.arange(numbers_columns))

    time_sub_ = pd.DataFrame(
        np.where(result_calc < 0.5, abs(target.timestamp.values[:, None] - outsider1.timestamp.values), np.nan),
        index=result_calc.index,
        columns=outsider1_timestamp.values.ravel())

    # check whether two ships are less than distance of 0.5 km
    for cols in result_calc.columns:
        result_calc[cols] = np.where(result_calc[cols] <= 0.5, result_calc[cols], np.nan)

    result_calc.columns = tuple(outsider1_latlon.values)
    result_calc = result_calc.apply(lambda x: pd.Series.round(x, 3))

    for col in time_sub_.columns:
        time_sub_[col] = np.where(((time_sub_[col] < 10) & (time_sub_[col] >= 0)), time_sub_[col], np.nan)

    target.reset_index(inplace=True, drop=True)
    result_calc.reset_index(inplace=True, drop=True)
    time_sub_.reset_index(inplace=True, drop=True)
    final = pd.concat([target, result_calc, time_sub_], axis=1)
    final = final.dropna(how='all', axis=1)

    '''
    If the encounter has happend, then this gives encounter data. 
    The file contains both encounters and non-encounter data. To get the exact
    time of the encounter, its duration and its closest distance, further analysis is needed in that output file.
    '''
    final.to_csv('TwoShipTogetherAnalysis.csv', index=0)
