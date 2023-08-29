from datetime import date, timedelta, datetime
from workalendar.europe import Germany
import pandas as pd
from interface import TourSelectionGUI, create_gui

def main():
    filename = "Personalplanung 2023.xlsx"
    create_gui()
    werktag = get_next_working_day(date.today())
    data = learn_data_from_excel(filename=filename, desired_date=werktag)
    print(data)
    


def get_next_working_day(current_day):
    cal = Germany()
    
    # Increment by one day to start
    next_day = current_day + timedelta(days=1)
    
    # While the next_day is a holiday or Sunday, keep moving to the next day
    while next_day.weekday() == 6 or cal.is_holiday(next_day): 
        next_day += timedelta(days=1)

    return next_day

def learn_data_from_excel(filename: str, desired_date: datetime.date) -> pd.DataFrame:
    """
    Extract specific data from the Excel file based on a given date.
    
    Args:
    - filename (str): Name of the Excel file to read.
    - desired_date (datetime.date): Desired date to extract data from.
    
    Returns:
    - DataFrame: Extracted data
    """

    # Read the excel file using pandas
    df = pd.read_excel(filename, engine='openpyxl', header=None)
    
    # Find the column that matches the provided date by searching row 4 (Python uses 0-based indexing)
    matching_col_idx = None
    for idx, value in enumerate(df.iloc[3]):
        
        if isinstance(value, datetime):
            datevalue = value.date()
            
            if datevalue == desired_date:
                matching_col_idx = idx
                break

    # If we didn't find a matching date, raise an error
    if matching_col_idx is None:
        raise ValueError(f"Date {desired_date} not found in the Excel file.")
    
    # Extract values from B20:C78 and the date column.
    extracted_data = df.iloc[19:78, [1, 2, matching_col_idx]]

    # Rename the columns
    extracted_data.columns = ['Name', 'Stammtour', 'Einsatz']

    # Filter out rows where 'Name' column cells are empty
    extracted_data = extracted_data[extracted_data['Name'].notnull()]

    return extracted_data


if __name__=="__main__":
    main()