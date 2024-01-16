import pandas as pd
from datetime import timedelta

def update_dates_in_excel(filename):
    # Read the excel file
    df = pd.read_excel(filename, engine='openpyxl', header=None)

    # Define the starting column index (D = 3) and row index for the dates (Row 4 = 3)
    start_col_idx = 3  # Column D
    row_idx = 3        # Row 4

    # Determine the ending column index based on the content of row 4
    end_col_idx = df.iloc[row_idx].last_valid_index()

    # Update the dates in the specified range
    for col in range(start_col_idx, end_col_idx + 1):
        cell_value = df.at[row_idx, col]
        if isinstance(cell_value, pd.Timestamp):
            df.at[row_idx, col] = cell_value + timedelta(days=365)

    # Write the updated DataFrame back to the Excel file
    df.to_excel(filename, index=False, header=None, engine='openpyxl')

# Usage
excel_filename = "Personalplanung 2023.xlsx"
update_dates_in_excel(excel_filename)
