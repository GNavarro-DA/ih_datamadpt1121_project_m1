from p_acquisition import acquisition as ac
from p_wrangling import wrangling as w
from p_analysis import analysis as an
import argparse

def argument_parser():
    parser = argparse.ArgumentParser(description='Set operation type')
    parser.add_argument("-r", "--results", help="function type. Options are: 'single' (just to check one place) and 'all' (to get the output of all places)" , type=str)
    args = parser.parse_args()
    return args

def main(arguments):
    print('\n\n')
    print("---------- Application Started it will last a few seconds, please don't close it ----------")
    print('\n')
    
    if arguments.results == 'single':
        df_places = ac.acquisition_places('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
        df_bikes = ac.acquisition_bikes('./data/bicimad_stations.csv')
        df_places_bikes = w.wrangling(df_places, df_bikes)
        result = an.analysis_single(df_places_bikes)
        print('result')
    elif arguments.results == 'all':
        df_places = ac.acquisition_places('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
        df_bikes = ac.acquisition_bikes('./data/bicimad_stations.csv')
        df_places_bikes = w.wrangling(df_places, df_bikes)
        result = an.analysis_all(df_places_bikes)
        result = 'result all'
    print('\n\n')
    print('---------- Application Closed ----------')

if __name__ == '__main__':
    main(argument_parser())
