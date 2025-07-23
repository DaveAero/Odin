import pandas as pd
import re

# Load the Excel file
mpd = pd.read_excel('data/MPDA320_R49_I00.xls', sheet_name="MPD", skiprows=2)

# Convert the 'APPLICABILITY' values to strings and split by 'OR'
split_conditions = mpd['APPLICABILITY'].apply(lambda x: re.split(r'\bOR\b', str(x).strip()))

# Create a DataFrame from the split conditions
conditions_df = pd.DataFrame(split_conditions.tolist())

# Rename columns to condition1, condition2, ...
conditions_df.columns = [f'condition{i+1}' for i in conditions_df.columns]

# Concatenate the original DataFrame with the new condition columns
mpd = pd.concat([mpd, conditions_df], axis=1)







# Compile the pattern
modPattern = re.compile(r'\b(PRE|POST)\b.*?(\d+)', re.IGNORECASE)

# For each condition column, create a dictionary column with matched values
for col in conditions_df.columns:
    dict_col = col + '_dict'

    def extract_dict(entry):
        if pd.isna(entry):
            return {}
        matches = modPattern.findall(entry)
        return {num: prepost.upper() for prepost, num in matches}

    mpd[dict_col] = mpd[col].apply(extract_dict)







# Save to Excel
mpd.to_excel("Test.xlsx", index=False)