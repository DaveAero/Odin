# Thor.py
# DAO for updating the database
# By David Burke


#########################################################################################
# Import required functions
import Frigg as initDBDAO
import regex as re
import pandas as pd
import numpy as np
import io

#########################################################################################
# The Main
# The Main AircraftDAO class
column_name = str("")
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

        ldnd = self.mpd[[
            "TASK\nNUMBER", "SOURCE TASK\nREFERENCE", "ACCESS", "PREPARATION", "ZONE", "DESCRIPTION", 
            "TASK CODE", "SAMPLE\nTHRESHOLD", "SAMPLE\nINTERVAL", "100%\nTHRESHOLD", "100%\nINTERVAL", 
            "SOURCE", "REFERENCE", "APPLICABILITY"
        ]]
        #print(ldnd.head())
        return ldnd
    
    def addMSN(self, msn):
        # Create a new column dynamically using the MSN value
        global column_name
        column_name = f"MSN {msn}"
        self.mpd[column_name] = ""

        # Apply the condition (from line 168-170)
        for index, row in self.mpd.iterrows():
            conditionlist = row["condition"]
            condition = conditionlist[0]
            if condition[0] == "ALL":
                self.mpd.at[index, column_name] = "Applicable"

        return self.mpd[column_name].tolist()
    
    def getAll(self):
        return self.mpd
 
    

    def getCopy(self):
        ldnd = self.mpd[[
            "TASK\nNUMBER", "SOURCE TASK\nREFERENCE", "ACCESS", "PREPARATION", "ZONE", "DESCRIPTION", 
            "TASK CODE", "SAMPLE\nTHRESHOLD", "SAMPLE\nINTERVAL", "100%\nTHRESHOLD", "100%\nINTERVAL", 
            "SOURCE", "REFERENCE", "APPLICABILITY", column_name
        ]]
    
        # Replace NaN and Infinity values before writing to Excel
        ldnd.replace([np.nan, float('nan'), float('inf'), float('-inf')], "", inplace=True)
    
        # Create an in-memory bytes buffer
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            ldnd.to_excel(writer, index=False, sheet_name='MPD')
    
            workbook = writer.book
            worksheet = writer.sheets['MPD']
    
            # Define formatting styles
            header_format = workbook.add_format({
                'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
                'fg_color': '#D7E4BC', 'border': 1, 'font_size': 12
            })
    
            cell_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
            left_align_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
    
            # Apply formatting to headers
            for col_num, value in enumerate(ldnd.columns):
                worksheet.write(0, col_num, value, header_format)
    
            # Adjust column width and apply cell formats
            column_widths = {
                "TASK\nNUMBER": 15, "SOURCE TASK\nREFERENCE": 20, "ACCESS": 15, "PREPARATION": 20,
                "ZONE": 10, "DESCRIPTION": 40, "TASK CODE": 10, "SAMPLE\nTHRESHOLD": 15,
                "SAMPLE\nINTERVAL": 15, "100%\nTHRESHOLD": 15, "100%\nINTERVAL": 15,
                "SOURCE": 15, "REFERENCE": 15, "APPLICABILITY": 20
            }
    
            for col_num, col_name in enumerate(ldnd.columns):
                width = column_widths.get(col_name, 15)
                worksheet.set_column(col_num, col_num, width)
    
                # Apply text alignment: Left for 'DESCRIPTION', Center for others
                cell_format_to_use = left_align_format if col_name == "DESCRIPTION" else cell_format
                for row_num in range(1, len(ldnd) + 1):
                    value = ldnd.iloc[row_num - 1, col_num]
    
                    # Ensure numbers are valid
                    if isinstance(value, (int, float)) and not np.isfinite(value):
                        worksheet.write(row_num, col_num, "", cell_format_to_use)  # Write empty string
                    else:
                        worksheet.write(row_num, col_num, value, cell_format_to_use)
    
        output.seek(0)
        return output
    
taskDAO = TaskDAO()

# Example usage
#if __name__ == "__main__":
#    taskDAO = TaskDAO()
#    taskDAO.typeChecker()
#    taskDAO.modsChecker()
#    df = taskDAO.getAll()
#    print(df.columns)