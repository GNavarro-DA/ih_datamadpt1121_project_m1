import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import re
from tkinter import *
from PIL import ImageTk, Image

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


def analysis_single_gui(df_places_bikes):
    def distance_meters(loc_start, loc_finish):
        return loc_start.distance(loc_finish)
    def row_filter(df, cat_var, cat_values):
        df = df[df[cat_var].isin(cat_values)]
        return df.reset_index(drop=True)
    
    new_window = Toplevel()
    e = Entry(new_window, bg="skyblue", borderwidth=0.5)
    e.pack()
    e.insert(0,'Enter your place')
    def submmit():
        newLabel = Label(new_window, text= "Your selected place is " + e.get())
        newLabel.pack()
        df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
        result = row_filter(df_places_bikes,'title',[e.get()]).sort_values(by='distance', ascending=True)[['address','title','distance']]
        result.to_csv('./output/single_result.csv')
        msg1 = "The nearest BiciMAD station is in: "
        address1 = result.iloc[0]['address']
        msg2 = ". It is approximately at " 
        distance1 = round(result.iloc[0]['distance'],1)
        msg3 =  " meters. "
        msg4 =  "\n\n" + "The next one is in "
        address2 = result.iloc[1]['address']
        msg5 = " at "
        distance2 = round(result.iloc[1]['distance'],1)
        msg6 = " meters"
        result_message = msg1 + address1 + msg2 + str(distance1) + msg3 + msg4 + address2 + msg5 + str(distance2) + msg6
        resultLabel = Label(new_window, text = result_message)
        resultLabel.pack()

    
    submmit_button = Button(new_window, text=" Confirm your place ", command=submmit).pack()
    

    
    next = input('Do you want to know the next 3 nearest station? (y/n): ')
    #if next == 'y':

    message = 'CLOSING APPLICATION'
    return message


def analysis_all_gui(df_places_bikes):
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