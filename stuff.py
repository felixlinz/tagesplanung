import pandas as pd
from datetime import timedelta


def update_dates_in_excel(filename):
    # Read the excel file
    df = pd.read_excel(filename, engine='openpyxl', header=None)

    # Update the dates
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x + timedelta(days=365) if isinstance(x, pd.Timestamp) else x)

    # Write the updated DataFrame back to the Excel file
    df.to_excel(filename, index=False, header=None, engine='openpyxl')

# Usage
excel_filename = "Personalplanung 2023.xlsx"
update_dates_in_excel(excel_filename)