import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

'''
This function creates a polygon shaped measurement area as shown in the thesis.
'''


def GenerateMeasurementBoundary(longitude, latitude):
    polygon = Polygon(
        [
            (19.67, 58.57),
            (19.31, 59.32),
            (20.64, 59.70),
            (22.25, 59.50),
            (21.87, 59.13),
            (21.15, 58.76)
        ])

    point_instance = Point((longitude, latitude))

    a = polygon.contains(point_instance)

    val = np.where(a, 0, np.nan)
    return pd.Series([val])
