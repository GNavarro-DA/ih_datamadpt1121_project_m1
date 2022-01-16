import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import re

def wrangling(df_places, df_bikes):
    def lat(x):
        x1 = re.sub('[[]|[]]','',x)
        x2 = re.split('[,]\s',x1)
        return float(x2[1])
    
    def long(x):
        x1 = re.sub('[[]|[]]','',x)
        x2 = re.split('[,]\s',x1)
        return float(x2[0])
    
    def to_mercator(lat, long):
        c = gpd.GeoSeries([Point(lat, long)], crs=4326)
        c = c.to_crs(3857)
        return c


    df_bikes['Latitude'] = df_bikes.apply(lambda x: lat(x['geometry_coordinates']),axis=1)
    df_bikes['Longitude'] = df_bikes.apply(lambda x: long(x['geometry_coordinates']),axis=1)
    df_places['location_place'] = df_places.apply(lambda x: to_mercator(x['location.latitude'], x['location.longitude']),axis=1)
    df_bikes['location_bikes'] = df_bikes.apply(lambda x: to_mercator(x['Latitude'], x['Longitude']),axis=1)
    df_places_bikes = df_places.assign(key=0).merge(df_bikes.assign(key=0), how='left', on='key')

    return df_places_bikes

