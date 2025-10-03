import pandas as pd
import re

# Load the Excel file
mpd = pd.read_excel('data/MPDA320_R49_I00.xls', sheet_name="MPD", skiprows=2)

# Convert the 'APPLICABILITY' values to strings and split by 'OR'
split_conditions = mpd['APPLICABILITY'].apply(lambda x: re.split(r'(?:\n\s*|\s+)?OR\b', str(x).strip()))

# Create a DataFrame from the split conditions
conditions_df = pd.DataFrame(split_conditions.tolist())

# Rename columns to condition1, condition2, ...
conditions_df.columns = [f'condition{i+1}' for i in conditions_df.columns]

# Concatenate the original DataFrame with the new condition columns
mpd = pd.concat([mpd, conditions_df], axis=1)







# Compile the pattern
typePattern = re.compile(r'\b(A318|A319|A320|A321)\b', re.IGNORECASE)
interiorPattern= re.compile(r'\b(-PAX|-VIP)\b', re.IGNORECASE)
varientPattern = re.compile(r'\b(A321-100|A321-PRE-FLEX|A321-NEO-PRE-FLEX|A321-POST-FLEX|A321-PRE-XLR|A321-POST-XLR)\b', re.IGNORECASE)
genPattern = re.compile(r'\b(NEO|CEO)\b', re.IGNORECASE)
wingPattern = re.compile(r'\b(CLASSIC WING|MODIFIED WING|RETRO WING|PRE-SPR-CURVE|POST-SPR-CURVE)\b', re.IGNORECASE)
modPattern = re.compile(r'\b(PRE|POST)\b.*?(\d+)', re.IGNORECASE)

# For each condition column, create a dictionary column with matched values
for col in conditions_df.columns:
    dict_col = col + '_dict'

    def extract_dict(entry):
        if pd.isna(entry):
            return {}
    
        result = {}
    
        # Match PRE/POST modifications
        matches = modPattern.findall(entry)
        if matches:
            result["MOD"] = []
            for prepost, num in matches:
                result["MOD"].append({prepost.upper(): num})
    
        # Match Aircraft Type
        type_match = typePattern.findall(entry)
        if type_match:
            result["Type"] = [t.upper() for t in type_match] if len(type_match) > 1 else type_match[0].upper()
    
        # Match Interior (-PAX / -VIP)
        interior_match = interiorPattern.findall(entry)
        if interior_match:
            result["Interior"] = [m.upper() for m in interior_match] if len(interior_match) > 1 else interior_match[0].upper()
    
        # Match Variant (e.g., A321-100, A321-POST-XLR, etc.)
        varient_match = varientPattern.findall(entry)
        if varient_match:
            result["Variant"] = [m.upper() for m in varient_match] if len(varient_match) > 1 else varient_match[0].upper()
    
        # Match Generation (NEO/CEO)
        gen_match = genPattern.findall(entry)
        if gen_match:
            result["Generation"] = [m.upper() for m in gen_match] if len(gen_match) > 1 else gen_match[0].upper()
    
        # Match Wing type
        wing_match = wingPattern.findall(entry)
        if wing_match:
            result["Wing"] = [m.upper() for m in wing_match] if len(wing_match) > 1 else wing_match[0].upper()
    
        return result

    mpd[dict_col] = mpd[col].apply(extract_dict)

# Save to Excel
cols_to_keep = ['APPLICABILITY', 'condition1']
for i in range(1, 10):
    cols_to_keep.append(f'condition{i}_dict')

mpd[cols_to_keep].to_excel("Test.xlsx", index=False)