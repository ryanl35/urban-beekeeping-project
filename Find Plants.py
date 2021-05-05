import pandas as pd
import os

# Obtain all of the files in the hive plant species data folder
files = []
csv_file_path = 'data/hive plant species data'
for r, d, f in os.walk(csv_file_path):
    for filename in f:
        files.append(filename)

# Go through each file and look for a specific plant name
def create_list_of_files_containing_plant_name(plant_name, files):
    '''
    :param plant_name: (str)
    :return: a list of strings of the file names
    '''
    csv_file_path = 'data/hive plant species data'
    files_containing_plant = []

    for filename in files:
        try:
            df = pd.read_csv(csv_file_path + '/' + filename)
            plants_in_file = df['Common Name'].tolist()

            # Append the files containing the specified plant to the list
            if plant_name in plants_in_file:
                files_containing_plant.append(filename)
        except:
            continue # This is to avoid any csv files that may have extension issues

    return files_containing_plant

create_list_of_files_containing_plant_name('Clovers', files)

