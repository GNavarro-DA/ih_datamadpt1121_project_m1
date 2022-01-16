import requests
import pandas as pd


def acquisition_places(url):
    url_datos_madrid = 'https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json'
    response = requests.get(url_datos_madrid)
    datos_json = response.json()
    df_places = pd.json_normalize(datos_json['@graph'])
    pd.set_option('display.max_colwidth',50)
    return df_places

def acquisition_bikes(path_file):
    df_bikes = pd.read_csv('../data/bicimad_stations.csv')
    return df_bikes