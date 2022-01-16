from p_acquisition import acquisition as ac
from p_wrangling import wrangling as w
from p_analysis import analysis as an

if __name__ == "__main__":
    df_places = ac.acquisition_places()
    df_bikes = ac.acquisition_bikes()
    df_places_bikes = w.wrangling()
    #argparse and conditions: 
    result = an.analysis_single()
    print(result)
    #or
    result = an.analysis_all()
    print(result)