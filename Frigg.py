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

def loki():
    file_path = 'data/MPDA320_R49_I00.xls'
    mpd = load_data(file_path)
    conditionColumn = []

    for value in mpd['APPLICABILITY'].apply(str):
        cut = re.split(r'\bOR\b', value)
        conditionList =[]

        if len(cut) == 1:
            clean_cut = re.split(r' |\n', cut[0].strip())  # Split by spaces and newlines
            clean_cut = [x for x in clean_cut if re.search(r'\w', x)]  # Keep only elements with text/numbers
            if clean_cut:  # Ensure non-empty lists are added
                    conditionList.append(clean_cut)
            conditionColumn.append(conditionList if conditionList else None)  # Avoid empty sublists

        else:
            for i in cut:
                clean_i = re.split(r' |\n', i.strip())  # Split by spaces and newlines
                clean_i = [x for x in clean_i if re.search(r'\w', x)]  # Keep only elements with text/numbers
                if clean_i:  # Ensure non-empty lists are added
                    conditionList.append(clean_i)
            conditionColumn.append(conditionList if conditionList else None)  # Avoid empty sublists

    # Assign the condition lists to a new column in the DataFrame
    mpd['condition'] = conditionColumn
    #print(mpd['condition'])

    #print(table['condition'])
    #mpd.to_excel("table.xlsx")
    return mpd

# Main script execution
if __name__ == "__main__":
    loki()