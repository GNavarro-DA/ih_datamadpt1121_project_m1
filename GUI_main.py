from p_acquisition import acquisition as ac
from p_wrangling import wrangling as w
from p_analysis import analysis as an
from tkinter import *
from PIL import ImageTk, Image


if __name__ == '__main__':
    root = Tk()
    root.title('WIMBA: Where Is My Bike App')
    description_message = "\n" + "Welcome to WIMBA, the perfect APP if you want to find the nearest BiciMAD station!" + "\n\n" + "Please, choose an option: " + "\n\n" + "Single Search: This will allow you to find nearest BiciMAD stations to one place of interest" + "\n"  + "All : This will allow you to find the nearest BiciMAD station to each place of interest" + "\n\n" + "*Please, note that this is a Beta Version App so it will last a few seconds in obtaining the result" + "\n"
    description = Label(root, text= description_message).pack()
    def single():
        df_places = ac.acquisition_places('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
        df_bikes = ac.acquisition_bikes('./data/bicimad_stations.csv')
        df_places_bikes = w.wrangling(df_places, df_bikes)
        result = an.analysis_single_gui(df_places_bikes)
        #print('result')
    def all_search():
        df_places = ac.acquisition_places('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
        df_bikes = ac.acquisition_bikes('./data/bicimad_stations.csv')
        df_places_bikes = w.wrangling(df_places, df_bikes)
        result_all= an.analysis_all_gui(df_places_bikes)
        #print('result all')
    
    single_button = Button(root, text=" Single Search ", command=single)
    single_button.pack()
    all_button = Button(root, text = " All ", command=all_search)
    all_button.pack()

    my_img = ImageTk.PhotoImage(Image.open("./pictures/bicimad.jpg"))
    my_lable = Label(root, image=my_img).pack()


    root.mainloop()
