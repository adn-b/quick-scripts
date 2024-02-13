import pandas as pd
from datetime import datetime

# Load the data
file_path = 'KBK Creditors.xlsx'
df = pd.read_excel(file_path)

# Function to convert date strings and assign correct year
def convert_date_with_year_stipulation(date_str):
    if not isinstance(date_str, str):
        return None

    # Normalize and clean the date string
    for suffix in ['th', 'st', 'nd', 'rd']:
        date_str = date_str.replace(suffix, '')
    date_str = date_str.strip()

    # Parse the date
    try:
        date_obj = datetime.strptime(date_str, '%d %B')
        year = "2022" if 6 <= date_obj.month <= 12 else "2023"
        return date_obj.replace(year=int(year))
    except ValueError as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None

# Convert all dates in the dataset
df['Converted Date'] = df.iloc[:, 0].apply(convert_date_with_year_stipulation)

# Separate the dataset into parts
df_already_sorted = df.iloc[:1092, :]
df_to_sort = df.iloc[1092:, :]

# Sort the part of the dataset that needs sorting
df_to_sort_sorted = df_to_sort.sort_values(by='Converted Date')

# Concatenate the already sorted part with the newly sorted part
df_final = pd.concat([df_already_sorted, df_to_sort_sorted])

# Save the final DataFrame to a new Excel file
df_final.to_excel('final_sorted_file.xlsx', index=False)
