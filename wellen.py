import csv
import os
from datetime import datetime

# Constants
CSV_DIR = "tour_data"
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

def get_weekday_filename():
    """
    Returns the CSV filename corresponding to today's weekday.
    """
    weekday = datetime.now().strftime('%A')  # This will return 'Monday', 'Tuesday', etc.
    return os.path.join(CSV_DIR, f"{weekday}.csv")

def save_state(tour_selections):
    """
    Saves the provided state to a CSV file.
    Args:
    - tour_selections: List of tuples, each containing (checkbox state, radio button state) for each tour.
    """
    with open(get_weekday_filename(), 'w', newline='') as file:
        writer = csv.writer(file)
        for tour_number, (chk_state, radio_state) in enumerate(tour_selections, 1):
            writer.writerow([tour_number, chk_state, radio_state])

def load_state():
    """
    Loads the saved state from a CSV file based on the current weekday.
    Returns a list of tuples, each containing (checkbox state, radio button state) for each tour.
    If no saved state exists for the current weekday, returns an empty list.
    """
    filename = get_weekday_filename()
    if not os.path.exists(filename):
        return []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        return [(int(row[0]), row[1] == "True", row[2]) for row in reader]
