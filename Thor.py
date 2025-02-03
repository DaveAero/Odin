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
        """Loads data from the initialized database and processes it using loki()."""
        db = initDBDAO.InitaliseDBDAO()
        db.getMPD()
        self.mpd = db.loki()
        
    def typeChecker(self):        
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
    
    def getLDND(self):
        """Loads, cleans, and retrieves selected columns from the database every time it's called."""

        ldnd = self.mpd[[
            "TASK\nNUMBER", "SOURCE TASK\nREFERENCE", "ACCESS", "PREPARATION", "ZONE", "DESCRIPTION", 
            "TASK CODE", "SAMPLE\nTHRESHOLD", "SAMPLE\nINTERVAL", "100%\nTHRESHOLD", "100%\nINTERVAL", 
            "SOURCE", "REFERENCE", "APPLICABILITY"
        ]]
        #print(ldnd.head())
        return ldnd
    
    def conditions(self):
        """Loads, cleans, and retrieves selected columns from the database every time it's called."""

        tasks = self.mpd[
            'condition'
        ]
        #print(ldnd.head())
        return tasks
        
    
taskDAO = TaskDAO()

# Example usage
#if __name__ == "__main__":
    #taskDAO = TaskDAO()
    #taskDAO.typeChecker()
    #taskDAO.modsChecker()
    #df = taskDAO.getAll()
    #print(df.shape)