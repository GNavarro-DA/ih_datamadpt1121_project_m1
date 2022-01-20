import webbrowser
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import re
from tkinter import *
from PIL import ImageTk, Image
import math
import webbrowser
import urllib.parse
from fuzzywuzzy import fuzz

def analysis_single(df_places_bikes):
    def distance_meters(loc_start, loc_finish):
        return loc_start.distance(loc_finish)
    def row_filter(df, cat_var, cat_values):
        df = df[df[cat_var].isin(cat_values)]
        return df.reset_index(drop=True)
    def address_match(imputed_address, saved_address):
        ratio = fuzz.token_set_ratio(imputed_address,saved_address)
        return ratio
    place_selected = [input('Introduce the Place of Interest: ')]
    print('\n\n')
    print('Ok, let me search bikes near that place!')
    print('\n\n')
    df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
    df_places_bikes['Address Match Ratio'] = df_places_bikes.apply(lambda x: address_match(place_selected, x['title']), axis=1)
    result = df_places_bikes.sort_values(by='Address Match Ratio', ascending=False).head()
    if result.iloc[0]['Address Match Ratio'] < 90:
        print('No results found for ', place_selected, '. Did you mean', result.iloc[0]['title'], '?')
    elif result.iloc[0]['Address Match Ratio'] >= 90:
        place_selected_fix = [result.iloc[0]['title']]
        result2 = row_filter(df_places_bikes,'title',place_selected_fix).sort_values(by='distance', ascending=True)[['title','address.street-address', 'name', 'address','distance']]
        final_df = result2.rename(columns={'title':'Place of Interest', 'address.street-address':'Place Address', 'name':'BiciMAD Station', 'address':'BiciMAD Location'})
        final_df.to_csv('./output/single_result.csv')
        print('/------------ FILE SAVED ---------------/')
        print('La estación BiciMAD más cercana está en: ', final_df.iloc[0]['BiciMAD Location'], '. Se encuentra a ', round(final_df.iloc[0]['distance'],1), 'metros', '\n', 'La siguiente se encuentra en ', final_df.iloc[1]['BiciMAD Location'], 'a ', round(final_df.iloc[1]['distance'],1), 'metros')
    
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
        msg3 =  " meters. " + "\n" + "This means "
        walking_time1 = math.ceil((distance1*60)/5000)
        msg4 = " minutes walking"

        msg5 =  "\n\n" + "The next one is in "
        address2 = result.iloc[1]['address']
        msg6 = " at "
        distance2 = round(result.iloc[1]['distance'],1)
        msg7 = " meters. " + "\n" + "This means "
        walking_time2 = math.ceil((distance2*60)/5000)
        msg8 = " minutes walking"

        result_message = msg1 + address1 + msg2 + str(distance1) + msg3 + str(walking_time1) + msg4 + msg5 + address2 + msg6 + str(distance2) + msg7 + str(walking_time2) + msg8
        
        resultLabel = Label(new_window, text = result_message)
        resultLabel.pack()

        def search_internet():
            url_encoded = urllib.parse.quote(address1)
            url = 'https://www.google.com/maps/place/' + url_encoded + 'MADRID'
            webbrowser.open(url)

        search_button = Button(new_window, text= "Look in Google Maps", command=search_internet).pack()

    
    submmit_button = Button(new_window, text=" Confirm your place ", command=submmit).pack()
    
    return 


def analysis_all_gui(df_places_bikes):
    def distance_meters(loc_start, loc_finish):
        return loc_start.distance(loc_finish)
    
    newWindow2 = Toplevel()
    newLabel2 = Label(newWindow2, text = "\n" + "Thank you for waiting" + "\n").pack()

    df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
    result_total = df_places_bikes.groupby(['title'])[['distance']].min().sort_values(by=('distance'), ascending=True)
    lower_distances = result_total.merge(df_places_bikes, how='inner', on=['title','distance'])[['title','address','distance']]
    lower_distances.to_csv('./output/all_lower_distances.csv')
    message = " YOUR FILE IS SAVED. THANKS FOR TRUSTING IN WIMBA " + "\n\n"
    result_allLabel = Label(newWindow2, text = message).pack()
    
    return