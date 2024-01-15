import csv
import os
from datetime import datetime, date, timedelta
import os
import pandas as pd
from workalendar.europe import Germany

def delete_data_file(file_path="data.csv"):
    """
    Deletes the data file if it exists.
    
    Args:
    - file_path (str): The path to the data file you want to delete. Default is "data.csv".
    
    Returns:
    - bool: True if the file was deleted successfully, False otherwise.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error while deleting the file: {e}")
            return False
    else:
        print(f"'{file_path}' does not exist.")
        return False


# Define constants
CSV_FILENAME = 'saved_data.csv'

def save_data(current_date, data_set):
    """
    Save data for the current date and weekday.
    The data_set is expected to be a set of tuples: (tour, checkbox_value, radio_value)
    """
    # print(current_date)
    weekday = current_date.strftime('%A')  # Extracts weekday name (e.g., "Tuesday")
    date_str = current_date.strftime('%Y-%m-%d')

    # Check if file exists
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Weekday', 'Date', 'Tour', 'Vorhanden', 'Welle'])  # header

    # Filter out old data for the same weekday and then append new data
    with open(CSV_FILENAME, 'r') as csvfile:
        lines = list(csv.reader(csvfile))
        lines = [line for line in lines if line[0] != 'Weekday' and line[0] != weekday]  # Exclude headers and old data

    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Weekday', 'Date', 'Tour', 'Vorhanden', 'Welle'])  # header
        writer.writerows(lines)  # Write back filtered data

        for tour, checkbox_val, radio_val in data_set:
            writer.writerow([weekday, date_str, tour, checkbox_val, radio_val])

def load_data(weekday):
    """
    Load saved data for a specific weekday.
    Returns the saved data as a set of tuples: (tour, checkbox_value, radio_value)
    """
    if not os.path.exists(CSV_FILENAME):
        return set()

    with open(CSV_FILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header

        data_set = set()
        for row in reader:
            if row[0] == weekday:
                tour, checkbox_val, radio_val = int(row[2]), int(row[3]), bool(row[4])
                data_set.add((tour, checkbox_val, radio_val))

        return data_set
    
    
csvtimefile = "wavetimes.csv"
    
def save_time_values(time_values):
    """
    Save time values to the CSV.
    
    Args:
    - time_values (tuple): Tuple of time values to save.
    """

    with open(csvtimefile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(time_values)



def load_time_values():
    """
    Load saved time values from the CSV.
    
    Returns:
    - tuple: A tuple containing the loaded time values.
    """
    if not os.path.exists(csvtimefile):
        with open(csvtimefile, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow("7:45,9:15")
            
            return ("7:45", "9:15")
                
            
    else:
        with open(csvtimefile, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                return tuple(row)


def learn_data_from_excel(desired_date: datetime.date) -> pd.DataFrame:
    """
    Extract specific data from the Excel file based on a given date.
    
    Args:
    - filename (str): Name of the Excel file to read.
    - desired_date (datetime.date): Desired date to extract data from.
    
    Returns:
    - DataFrame: Extracted data
    """
    
    filename = "Personalplanung 2023.xlsx"

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


def get_next_working_day(current_day):
    cal = Germany()
    
    # Increment by one day to start
    next_day = current_day + timedelta(days=1)
    
    # While the next_day is a holiday or Sunday, keep moving to the next day
    while next_day.weekday() == 6 or cal.is_holiday(next_day): 
        next_day += timedelta(days=1)

    return next_day



"""if __name__=="__name__":
    main()"""