import requests
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import re
import webbrowser
from tkinter import *
from PIL import ImageTk, Image
import math
import urllib.parse
from fuzzywuzzy import fuzz


def acquisition_places(url):
    response = requests.get(url)
    datos_json = response.json()
    df_places = pd.json_normalize(datos_json['@graph'])
    pd.set_option('display.max_colwidth',50)
    return df_places

def acquisition_bikes(path_file):
    df_bikes = pd.read_csv(path_file)
    return df_bikes

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

def analysis_single_gui(df_places_bikes):
    def distance_meters(loc_start, loc_finish):
        return loc_start.distance(loc_finish)
    def row_filter(df, cat_var, cat_values):
        df = df[df[cat_var].isin(cat_values)]
        return df.reset_index(drop=True)
    def address_match(imputed_address, saved_address):
        ratio = fuzz.token_set_ratio(imputed_address,saved_address)
        return ratio
    
    new_window = Toplevel()
    e = Entry(new_window, bg="skyblue", borderwidth=0.5)
    e.pack()
    e.insert(0,'Enter your place')
    def submmit():

        newLabel = Label(new_window, text= "Your selected place is " + e.get())
        newLabel.pack()
        df_places_bikes['distance'] = df_places_bikes.apply(lambda x: distance_meters(x['location_place'], x['location_bikes']),axis=1)
        df_places_bikes['Address Match Ratio'] = df_places_bikes.apply(lambda x: address_match(e.get(), x['title']), axis=1)
        result = df_places_bikes.sort_values(by='Address Match Ratio', ascending=False).head()
        if result.iloc[0]['Address Match Ratio'] < 90:
            no_result_message = 'No results found for ' + e.get() + '\n' + '. Did you mean ' + result.iloc[0]['title'] + '?'
            no_result_label = Label(new_window, text=no_result_message).pack()
        elif result.iloc[0]['Address Match Ratio'] >= 90:
            place_selected_fix = [result.iloc[0]['title']]
            result2 = row_filter(df_places_bikes,'title',place_selected_fix).sort_values(by='distance', ascending=True)[['title','address.street-address', 'name', 'address','distance']]
            final_df = result2.rename(columns={'title':'Place of Interest', 'address.street-address':'Place Address', 'name':'BiciMAD Station', 'address':'BiciMAD Location'})
            final_df.to_csv('./output/single_result.csv')
            final_df.to_csv('./output/single_result.csv')

            msg1 = "The nearest BiciMAD station is in: "
            address1 = result2.iloc[0]['address']
            msg2 = ". It is approximately at " 
            distance1 = round(result2.iloc[0]['distance'],1)
            msg3 =  " meters. " + "\n" + "This means "
            walking_time1 = math.ceil((distance1*60)/5000)
            msg4 = " minutes walking"

            msg5 =  "\n\n" + "The next one is in "
            address2 = result2.iloc[1]['address']
            msg6 = " at "
            distance2 = round(result2.iloc[1]['distance'],1)
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

if __name__ == '__main__':
    root = Tk()
    root.title('WIMBA: Where Is My Bike App')
    description_message = "\n" + "Welcome to WIMBA, the perfect APP if you want to find the nearest BiciMAD station!" + "\n\n" + "Please, choose an option: " + "\n\n" + "Single Search: This will allow you to find nearest BiciMAD stations to one place of interest" + "\n"  + "All : This will allow you to find the nearest BiciMAD station to each place of interest" + "\n\n" + "*Please, note that this is a Beta Version App so it will last a few seconds in obtaining the result" + "\n"
    description = Label(root, text= description_message).pack()
    def single():
        df_places = acquisition_places('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
        df_bikes = acquisition_bikes('./data/bicimad_stations.csv')
        df_places_bikes = wrangling(df_places, df_bikes)
        result = analysis_single_gui(df_places_bikes)
        #print('result')
    def all_search():
        df_places = acquisition_places('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
        df_bikes = acquisition_bikes('./data/bicimad_stations.csv')
        df_places_bikes = wrangling(df_places, df_bikes)
        result_all= analysis_all_gui(df_places_bikes)
        #print('result all')
    
    single_button = Button(root, text=" Single Search ", command=single)
    single_button.pack()
    all_button = Button(root, text = " All ", command=all_search)
    all_button.pack()

    my_img = ImageTk.PhotoImage(Image.open("./pictures/bicimad.jpg"))
    my_lable = Label(root, image=my_img).pack()


    root.mainloop()