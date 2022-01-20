# WIMBA README file

![Image](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.eldiario.es%2Fopinion%2Ftribuna-abierta%2Fverdadera-historia-bicimad_129_2206352.html&psig=AOvVaw2A76gJ-Vq0C7d4x1gAjoU_&ust=1642788919895000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCKDm0eT3wPUCFQAAAAAdAAAAABAD)

---

## **About this project:**
*Here, Ironhack Data Analysis Project 1 is introduced. In this README file you can read all information related to this project.*


## **DESCRIPTION:**

### :raising_hand: **Name** 

**WIMBA:** *Where Is My Bike App* 
***Author:*** Gonzalo Navarro Fernández

### :baby: **Status**

This is a Beta Version of an App used as **deliverable** for *Ironhack Data Analysis First Project*. 
*Date of presentation is Jan the 22nd of 2022 on Ironhack Campus Madrid*

### :running: **One-liner**
Just one-liner per app:
* There is a main.py applications to be used in the CLI. This App has two possible actions made with `argparse`library: (1) Given a Place of Interest (POI) the app returns the nearest BiciMAD station; and (2) The app returns the nearest BiciMAD station of all POI in a Database. 

* Also, there is a GUI_main.py app to be used as an .exe field build with a simple GUI that allows the user to choice between both options by clicking buttons. This was made with `tkinter`library.

Both apps run properly. 

### :computer: **Technology stack**
**Primary programming language:** Python
**Main libraries:** `requests`, `pandas`, `tkinter`, `re`, `geopandas`, `shapely.geometry`, `urllib.parse`, `webbrowser`, `math`,`PIL`.
**Details of the software:** This software is intended as standalone, but one static database is needed to run properly *(BiciMAD database)*. This data are included in the data folder of this repository. 


### :boom: **Core technical concepts and inspiration**
The main idea of this project was given to all alumni of the course as a project goal. But when I started to work on the app I decided to design it as functional and real as possible. That was the reason to make a Beta version of a Desktop App with a GUI. 

This App tries to solve the problem of finding a Bike Station near a selected POI or all POI recorded in a database. This Beat Version App uses as POI database all Health Care Centers of Madrid recorded in its Open Data portal [See it here](https://datos.madrid.es/nuevoMadrid/swagger-ui-master-2.2.10/dist/index.html?url=/egobfiles/api.datos.madrid.es.json#/). 

Of course, this is extrapolable to other databases.

### :wrench: **Configuration**
This App runs properly with Python 3.7 version. 
Only requirement is to have all libraries specified above. Note that some of them have to be installed previously in the working environment.


### :see_no_evil: **Usage**
**1. Use of CLI app**
Run the main.py app in your CLI with -h or -help to see options. 

Only using the 'single' after the `-r` flag, other input is needed: the selected POI. 

If the user selects the 'all' argument after the `-r` flag, no more input is needed. 

**2. Use of GUI app**
Double Click on the App icon and the App will run.

Then only input needed is by cliking the 'Single Search' button. The App will ask for a POI. 


### :file_folder: **Folder structure**
```
└── project
    ├── __trash__
    ├── .gitignore
    ├── README_project1.md
    ├── main.py
    ├── GUI_main.py
    ├── data
    │   ├── bicimad_stations.csv
    │   └── bicipark_stations.csv
    │   └── turnosmadrid_guardia_2022.xlsx
    │   └── bicimad_stations.json
    │   └── bicipark_stations.json
    ├── notebooks
    │   ├── For Practice.ipynb
    │   └── GUI - APP.ipynb
    │   └── Just to track time of total code.ipynb
    │   └── notebook_project1.ipynb
    ├── output
    ├── p_acquisition
    │   ├── __pycache__
    │   └── acquisition.py
    ├── p_analysis
    │   ├── __pycache__
    │   └── analysis.py
    ├── p_wrangling
    │   ├── __pycache__
    │   └── wrangling.py
    ├── pictures
    │   └── bicimad.jpeg
    └── sql_queries
        └── getting_tables.sql

```


### :shit: **ToDo**
* Connect to the BiciMAD API to get Real Time results and improve features of WIMBA.
* Allow to the GUI windows to scroll
* Improve the GUI 
* Improve the time to response of the App (currently it needs 30 seconds approx)



### :love_letter: **Contact info**
Getting help, getting involved, hire me please.

---
