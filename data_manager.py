import csv
import os
from datetime import datetime

# Define constants
CSV_FILENAME = 'saved_data.csv'

def save_data(current_date, tour_amount, data_set):
    """
    Save data for the current date and weekday.
    The data_set is expected to be a set of tuples: (tour, checkbox_value, radio_value)
    """
    weekday = current_date.strftime('%A')  # Extracts weekday name (e.g., "Tuesday")
    date_str = current_date.strftime('%Y-%m-%d')

    # Check if file exists
    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Weekday', 'Date', 'Tour', 'Checkbox_Value', 'Radio_Value'])  # header

    # Filter out old data for the same weekday and then append new data
    with open(CSV_FILENAME, 'r') as csvfile:
        lines = list(csv.reader(csvfile))
        lines = [line for line in lines if line[0] != 'Weekday' and line[0] != weekday]  # Exclude headers and old data

    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Weekday', 'Date', 'Tour', 'Checkbox_Value', 'Radio_Value'])  # header
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
                tour, checkbox_val, radio_val = int(row[2]), int(row[3]), int(row[4])
                data_set.add((tour, checkbox_val, radio_val))

        return data_set
