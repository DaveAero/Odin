# Frigg.py
# Used to initalise the database from Excel into Python Pandas DB
# By David Burke


#########################################################################################
# Import required functions
#from Thor import ???
import pandas as pd
import re

# The Main AircraftDAO class
#class InitalizeDBDAO: 
    #########################################################################################
    ### data location

    ### Creating the Database
def load_data(file_path):
    mpd = pd.read_excel(file_path, sheet_name="MPD", skiprows=2)
    return mpd

def loki(table):
    conditionColumn = []
    conditionList = []

    for value in table['APPLICABILITY'].apply(str):
        cut = re.split(r'\bOR\b', value)
        condition = []

        for i in cut:
            clean_i = re.split(r' |\n', i.strip())  # Split by spaces and newlines, remove extra spaces
            condition.extend(clean_i)

        # Append the condition list to the new column list
        cleaned_list = [item for item in condition if item.strip()]
        conditionColumn.append(cleaned_list)

        # Store unique configurations
        if cleaned_list not in conditionList:
            conditionList.append(cleaned_list)

    # Assign the condition lists to a new column in the DataFrame
    table['condition'] = conditionColumn

    print(table['condition'])
    table.to_excel("table.xlsx")

# Main script execution
if __name__ == "__main__":
    file_path = 'data/MPDA320_R49_I00.xls'
    mpd = load_data(file_path)
    #print(mpd.head(20))
    loki(mpd)