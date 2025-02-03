# Frigg.py
# Used to initalise the database from Excel into Python Pandas DB
# By David Burke


#########################################################################################
# Import required functions
#from Thor import ???
import pandas as pd
import re

# The Main AircraftDAO class
class InitaliseDBDAO:
    def __init__(self, file_path='data/MPDA320_R49_I00.xls'):
        """Initializes the database with the given file path."""
        self.file_path = file_path
        self.mpd = None
        self.mpd = pd.read_excel(self.file_path, sheet_name="MPD", skiprows=2)
    
    def loki(self):
        """Processes the 'APPLICABILITY' column to extract conditions."""
        if self.mpd is None:
            raise ValueError("Data not loaded. Call loadData() first.")
        
        condition_column = []  # List to store extracted conditions
        
        for value in self.mpd['APPLICABILITY'].apply(str):  # Convert values to string for processing
            cut = re.split(r'\bOR\b', value)  # Split by 'OR' keyword
            condition_list = []  # Temporary list to store conditions for each row

            if len(cut) == 1:
                # If there is no 'OR', clean up the condition string
                clean_cut = re.split(r' |\n', cut[0].strip())  # Split by spaces and newlines
                clean_cut = [x for x in clean_cut if re.search(r'\w', x)]  # Remove empty elements
                if clean_cut:
                    condition_list.append(clean_cut)  # Add non-empty conditions
                condition_column.append(condition_list if condition_list else None)
            else:
                # If multiple conditions exist, process each separately
                for i in cut:
                    clean_i = re.split(r' |\n', i.strip())  # Split by spaces and newlines
                    clean_i = [x for x in clean_i if re.search(r'\w', x)]  # Remove empty elements
                    if clean_i:
                        condition_list.append(clean_i)  # Add non-empty conditions
                condition_column.append(condition_list if condition_list else None)
        
        self.mpd['condition'] = condition_column  # Store extracted conditions in a new column
        return self.mpd
    
    def getMPD(self):
        """Returns the processed DataFrame."""
        if self.mpd is None:
            raise ValueError("Data not loaded or processed. Call loadData() and loki() first.")
        return self.mpd

initaliseDBDAO = InitaliseDBDAO()