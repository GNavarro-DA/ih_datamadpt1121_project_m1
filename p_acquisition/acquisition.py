import requests
import pandas as pd


def acquisition_places(url):
    response = requests.get(url)
    datos_json = response.json()
    df_places = pd.json_normalize(datos_json['@graph'])
    pd.set_option('display.max_colwidth',50)
    return df_places

def acquisition_bikes(path_file):
    df_bikes = pd.read_csv(path_file)
    return df_bikes