import ssl
import certifi
import geopy.geocoders
from  geopy.geocoders import Nominatim
import pandas as pd
import csv

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

def coordFinder(cityName, stateName):
    geolocator = Nominatim(user_agent="coordinateFinder")
    city = cityName
    state = stateName

    try:
        loc = geolocator.geocode(city+', '+ state)
        return (loc.latitude, loc.longitude)
    except:
        print("Not a valid city:", city)

def allCoords(df):

    latitudeList = []
    longitudeList = []

    for i in range(df["City"].count()):

        # print(i)
        city = df["City"][i]
        # print(city)
        state = df["State"][i]
        # print(state)

        latLonTup = coordFinder(city, state)

        try:
            latitude = latLonTup[0]
            latitudeList.append(latitude)
            longitude = latLonTup[1]
            longitudeList.append(longitude)

            # print(latitude)
            # print(longitude)

        except:
            # print("Not a valid city:", city)
            longitudeList.append("N/A")
            latitudeList.append("N/A")

    # for latitude in latitudeList:
        # print(latitude)

    # for longitude in longitudeList:
        # print(longitude)

    df["Latitude"] = latitudeList
    df["Longitude"] = longitudeList

    print(len(latitudeList))
    print(len(longitudeList))


def addHealth(df, healthDF):

    sizeOfDF = df["City"].count() # 121
    sizeOfHealthDF = healthDF["Tube ID#"].count() # 39
    health = ["N/A"] * sizeOfDF

    for i in range(sizeOfDF):
                
        currID = df["Hive ID"][i]
            
        for j in range(sizeOfHealthDF):
            if (currID == healthDF["Tube ID#"][j]):
                del health[i]
                health.insert(i, healthDF["Condition"][j])

    df["Health"] = health
    
        
df = pd.read_csv('data/ids_cities_states.csv')
dfHealth = pd.read_csv('data/cleaned_health_data.csv')

# allCoords(df) # function finds lat and lon of cities
cleanedDf = pd.read_csv('data/ids_cities_with_coords.csv')
# allCoords(cleanedDf)
addHealth(cleanedDf, dfHealth)
cleanedDf.to_csv('data/ids_cities_with_coords.csv', index=False)
