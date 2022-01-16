import requests
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import re

def analysis_single(df_places_bikes):
    def distance_meters(loc_start, loc_finish):
        return loc_start.distance(loc_finish)
    def row_filter(df, cat_var, cat_values):
        df = df[df[cat_var].isin(cat_values)]
        return df.reset_index(drop=True)
    df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
    place_selected = [input('Introduce the Place of Interest: ')]
    result = row_filter(df_places_bikes,'title',place_selected).sort_values(by='distance', ascending=True)[['address','title','distance']]
    ## save csv file
    message = print('La estación BiciMAD más cercana está en: ', result.iloc[0]['address'], '. Se encuentra a ', round(result.iloc[0]['distance'],1), 'metros', '\n', 'La siguiente se encuentra en ', result.iloc[1]['address'], 'a ', round(result.iloc[1]['distance'],1), 'metros')
    #if there is any error in the message, save values and make other return clause
    return message


def analysis_all(df_places_bikes):
    def distance_meters(loc_start, loc_finish):
        return loc_start.distance(loc_finish)
    def row_filter(df, cat_var, cat_values):
        df = df[df[cat_var].isin(cat_values)]
        return df.reset_index(drop=True)
    df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
    result_total = df_places_bikes.groupby(['title'])[['distance']].min().sort_values(by=('distance'), ascending=True)
    lower_distances = result_total.merge(df_places_bikes, how='inner', on=['title','distance'])[['title','address','distance']]
    ## save csv file
    message = '/------------ FILE SAVED ---------------/'
    return message
