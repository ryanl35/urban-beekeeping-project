import math
import pandas as pd
import csv

def haversineFormula(latIn1, lonIn1, latIn2, lonIn2):
    # radius of the Earth
    R = 6371.0

    lat1 = math.radians(latIn1)
    lat2 = math.radians(latIn2)
    dlat = math.radians(latIn2 - latIn1)
    dlon = math.radians(lonIn2 - lonIn1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + (math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * math.sin(dlon / 2))

    # Haversine formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    # print(distance) # in km
    return distance



def closeProximity(df):

    hiveID = []
    city = []
    state = []
    lon = []
    lat = []
    health =[]

    # dfColumnSize = df["City"].count()

    tooClose = 30;
    i = 0;
    
    while (i < df["City"].count()):
        iLat = df["Latitude"][i]
        iLon = df["Longitude"][i]

        j = 0;
        
        while (j < df["City"].count()):
            jLat = df["Latitude"][j]
            jLon = df["Longitude"][j]

            if (df["City"][i] != df["City"][j]):
                if (haversineFormula(iLat, iLon, jLat, jLon) <= tooClose):
                    df.drop([j], inplace=True)
                    df = df.reset_index(drop=True)
                    
            j = j + 1

        i = i + 1

    for k in range(df["City"].count()):
        hiveID.append(df["Hive ID"][k])
        city.append(df["City"][k])
        state.append(df["State"][k])
        lon.append(df["Longitude"][k])
        lat.append(df["Latitude"][k])
        health.append(df["Health"][k])

    citiesToKeep = pd.DataFrame(columns=["Hive ID", "City", "State", "Longitude", "Latitude", "Health"])
    citiesToKeep["Hive ID"] = hiveID
    citiesToKeep["City"] = city
    citiesToKeep["State"] = state
    citiesToKeep["Longitude"] = lon
    citiesToKeep["Latitude"] = lat
    citiesToKeep["Health"] = health
    
    return citiesToKeep

cleanedDf = pd.read_csv('data/ids_cities_with_coords.csv')
closeProximity(cleanedDf).to_csv('data/cities_to_plot.csv', index=False)
