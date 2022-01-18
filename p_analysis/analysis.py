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
    place_selected = [input('Introduce the Place of Interest: ')]
    print('\n\n')
    print('Ok, let me search bikes near that place!')
    print('\n\n')
    df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
    result = row_filter(df_places_bikes,'title',place_selected).sort_values(by='distance', ascending=True)[['address','title','distance']]
    result.to_csv('./output/single_result.csv')
    print('/------------ FILE SAVED ---------------/')
    print('The nearest BiciMAD station is in: ', result.iloc[0]['address'], '. It is approximately at ', round(result.iloc[0]['distance'],1), 'meters', '\n', 'The next one is in ', result.iloc[1]['address'], 'at ', round(result.iloc[1]['distance'],1), 'metes')
    next = input('Do you want to know the next 3 nearest station? (y/n): ')
    #if next == 'y':

    message = 'CLOSING APPLICATION'
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
    lower_distances.to_csv('./output/all_lower_distances.csv')
    message = '/------------ FILE SAVED ---------------/'
    return message
