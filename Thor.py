# Thor.py
# DAO for updating the database
# By David Burke


#########################################################################################
# Import required functions
import Frigg as initDBDAO
import regex as re
import pandas as pd

#########################################################################################
# The Main
# The Main AircraftDAO class
class TaskDAO:
    def __init__(self):
        """Initializes the TaskDAO object."""
        self.mpd = None
    
    def loadData(self):
        """Loads data from the initialized database and processes it using loki()."""
        db = initDBDAO.InitaliseDBDAO()
        db.loki()
        self.mpd = db.getMPD()
    
    def typeChecker(self):
        """Checks and extracts aircraft types (A318, A319, A320, A321) from the 'condition' column."""
        if self.mpd is None:
            raise ValueError("Data not loaded. Call loadData() first.")
        
        typePattern = re.compile(r'(?<=\')\bA318\b|\bA319\b|\bA320\b|\bA321\b(?=\')', re.IGNORECASE)
        
        def Mjolnir(mpdCondition):
            results = []
            for i in mpdCondition:
                condition = {}
                matches = typePattern.findall(str(i))
                if matches:
                    condition[matches[0]] = 0
                else:
                    condition['0'] = 0
                results.append(condition)
            return results

        self.mpd['type'] = self.mpd['condition'].apply(Mjolnir)
        #print(self.mpd['type'])
    
    def modsChecker(self):
        """Checks and extracts modification types (PRE, POST) along with their corresponding numbers."""
        if self.mpd is None:
            raise ValueError("Data not loaded. Call loadData() first.")
        
        modPattern = re.compile(r'(\bPRE\b|\bPOST\b)\', \'(\d+)', re.IGNORECASE)
        
        def Stormbreaker(mpdCondition):
            results = []
            for i in mpdCondition:
                condition = {}
                modmatches = modPattern.findall(str(i))
                if modmatches:
                    for prefix, number in modmatches:
                        condition[number] = prefix
                else:
                    condition['0'] = 0
                results.append(condition)
            return results

        self.mpd['mod'] = self.mpd['condition'].apply(Stormbreaker)
        #print(self.mpd['mod'])
    
    def getAll(self):
        """Loads, cleans, and retrieves selected columns from the database every time it's called."""
        self.loadData()
        ldnd = self.mpd[[
            "TASK\nNUMBER", "SOURCE TASK\nREFERENCE", "ACCESS", "PREPARATION", "ZONE", "DESCRIPTION", 
            "TASK CODE", "SAMPLE\nTHRESHOLD", "SAMPLE\nINTERVAL", "100%\nTHRESHOLD", "100%\nINTERVAL", 
            "SOURCE", "REFERENCE", "APPLICABILITY"
        ]]
        #print(ldnd.head())
        return ldnd
    
taskDAO = TaskDAO()

# Example usage
#if __name__ == "__main__":
    #taskDAO = TaskDAO()
    #taskDAO.typeChecker()
    #taskDAO.modsChecker()
    #df = taskDAO.getAll()
    #print(df.shape)