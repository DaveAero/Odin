# Thor.py
# DAO for updating the database
# By David Burke


#########################################################################################
# Import required functions
import Frigg as initaliseDB
import regex as re
import pandas as pd

#########################################################################################
# The Main
# The Main AircraftDAO class
class Magic:
    def typeChecker(mpd):
        # Updated regex pattern to include all specified note types
        typePattern = re.compile(r'(?<=\')\bA318\b|\bA319\b|\bA320\b|\bA321\b(?=\')', re.IGNORECASE)

        def Mjolnir(mpdCondition):
            results = []
            #print(mpdCondition)
            for i in mpdCondition:
                condition = {}
                matches = typePattern.findall(str(i))
                if matches:
                    condition['{}'.format(matches[0])] = 0
                else:
                    condition['0'] = 0
                results.append(condition)
            return results

        mpd['type'] = mpd['condition'].apply(Mjolnir)
        print(mpd['type'])
        return mpd

    def modsChecker(mpd):
        # Updated regex pattern to include all specified note types
        modPattern = re.compile(r'(\bPRE\b|\bPOST\b)\', \'(\d+)', re.IGNORECASE)

        def Stormbreaker(mpdCondition):
            results = []
            for i in mpdCondition:
                #print(i)
                condition = {}
                modmatches = modPattern.findall(str(i))
                #print("Prematches:{}".format(prematches))
                if modmatches:
                     for prefix, number in modmatches:
                        condition[number] = prefix  # Store the prefix as value
                else:
                    condition['0'] = 0  # Default value when no match found
                results.append(condition)
            return results

        mpd['mod'] = mpd['condition'].apply(Stormbreaker)
        print(mpd['mod'])
        return mpd
    
    def getAll():
        mpd = pd.DataFrame(initaliseDB.loki())
        ldnd = mpd[["TASK\nNUMBER", "SOURCE TASK\nREFERENCE", "ACCESS", "PREPARATION", "ZONE", "DESCRIPTION", "TASK CODE", "SAMPLE\nTHRESHOLD", "SAMPLE\nINTERVAL", "100%\nTHRESHOLD", "100%\nINTERVAL", "SOURCE", "REFERENCE", "APPLICABILITY"]]
        print(ldnd.head())
        return ldnd

if __name__ == "__main__":
    dataDAO = Magic()