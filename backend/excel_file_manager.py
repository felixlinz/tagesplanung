import csv
import os
from datetime import datetime, date, timedelta
import os
import pandas as pd
from workalendar.europe import Germany
import math

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
    
class TimeDataManager:
    def __init__(self, filename="startzeiten.csv"):
        self.filename = filename
        self.times = {}
        if not os.path.exists(self.filename):
            self.create_initial_file()

    def read_times(self):
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            self.times = [(row[0], row[1]) for row in reader]
        return self.times

    def save_times(self, new_times):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for label, time in new_times:
                writer.writerow([label, time])



class DailyHoursManager:
    def __init__(self, filename="daily_hours.csv"):
        self.filename = filename
        self.hours = {}

    def read_hours(self):
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            self.hours = [(row[0], row[1]) for row in reader]
        return self.hours

    def save_hours(self, new_hours):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for day, hours in new_hours:
                writer.writerow([day, hours])
                
class DailyToursManager:
    def __init__(self, base_filename="data_{weekday}.csv"):
        self.base_filename = base_filename

    def _get_filename(self, weekday):
        """
        Generate a filename based on the given weekday.
        """
        return self.base_filename.format(weekday=weekday.lower())

    def read_data(self, weekday):
        """
        Read data from the file corresponding to the given weekday.
        """
        filename = self._get_filename(weekday)
        if not os.path.exists(filename):
            return []  # Return an empty list if the file does not exist
        
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            return [(row[0], int(row[1]), row[2]) for row in reader]

    def save_data(self, data, weekday):
        """
        Save the given data to the file corresponding to the given weekday.
        """
        filename = self._get_filename(weekday)
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in data:
                writer.writerow(item)
                


class ExcelManager:
    """Read and extract planning data from an Excel file."""

    def __init__(self, date, filename: str = "Personalplanung 2023.xlsx"):
        self.filename  = filename
        self.date      = date 
        self.dataframe = self.learn_data_from_excel(self.date) 
        self.sorted    = self.sort_workers()
        self.dict      = self.return_dict()
        
        
    def get_next_dates(self):
        daterow = [self.today]
        for _ in range(5):
            daterow.append(self.get_next_file_day(daterow[-1]))
            
        return daterow        
        
    
    def learn_data_from_excel(self, desired_date: date) -> pd.DataFrame:
        """
        Extract specific data from the Excel file based on a given date.

        Args:
            desired_date (datetime.date): Desired date to extract data from.

        Returns:
            pd.DataFrame: Extracted data for the given date.
        """
        # read file
        df = pd.read_excel(self.filename, engine="openpyxl", header=None)

        # find matching column in row 4 (index 3)
        matching_col_idx = None
        for idx, value in enumerate(df.iloc[3]):
            if isinstance(value, datetime) and value.date() == desired_date:
                matching_col_idx = idx
                break

        if matching_col_idx is None:
            raise ValueError(f"Date {desired_date} not found in {self.filename}")

        # extract relevant range and rename columns
        extracted_data = df.iloc[19:132, [1, 2, matching_col_idx]]
        extracted_data.columns = ["Name", "Stammtour", "Einsatz"]
        extracted_data = extracted_data[extracted_data["Name"].notnull()]

        return extracted_data

    def return_dataframe(self):
        return self.dataframe

    def return_dict(self):
        return self.dataframe.to_dict(orient="records")
    
    def sort_workers(self: bool = False):
        df = self.dataframe

        # Stammfahrer: numeric Stammtour & Einsatz == 1
        df_numeric_stammtour = df[pd.to_numeric(df["Stammtour"], errors="coerce").notna()]
        sorted_df_numeric = (
            df_numeric_stammtour[df_numeric_stammtour["Einsatz"] == 1]
            .sort_values(by="Stammtour")
            .reset_index(drop=True)
        )

        # Springer
        sorted_df_s = df[(df["Stammtour"] == "s") & (df["Einsatz"] == 1)]

        # Special Einsatz categories
        sorted_df_fd = df[df["Einsatz"] == "FD"]
        sorted_df_sd = df[df["Einsatz"] == "SD"]
        sorted_df_id = df[df["Einsatz"] == "ID"]
        sorted_df_fa = df[df["Einsatz"] == "FA"]
        sorted_df_e = df[df["Einsatz"] == "E"]
        sorted_df_df = df[df["Einsatz"] == "df"]

        # 🧠 Abrufer: Stammtour == "AB" and Einsatz ∈ {1, "E"}
        sorted_df_abrufer = df[
            (df["Stammtour"] == "AB") &
            (df["Einsatz"].isin([1, "E"]))
        ].reset_index(drop=True)

        # Collect all groups
        dataframes = {
            "Stammfahrer": sorted_df_numeric,
            "Springer": sorted_df_s,
            "Frühdienst": sorted_df_fd,
            "Spätdienst": sorted_df_sd,
            "Innendienst": sorted_df_id,
            "Firmen": sorted_df_fa,
            "Einweisung": sorted_df_e,
            "Dienstfrei": sorted_df_df,
            "Abrufer": sorted_df_abrufer,
        }

        # Convert all to JSON-ready dicts
        json_ready = {
            key: df_.to_dict(orient="records")
            for key, df_ in dataframes.items()
        }

        return json_ready


                
                
   
class DateManager: 
    def __init__(self, filename: str = "Personalplanung 2023.xlsx"):
        self.filename = filename
        self.date     = date  
        
    def get_next_working_day(self,current_day):
        cal = Germany()
        
        # Increment by one day to start
        next_day = current_day + timedelta(days=1)
        
        # While the next_day is a holiday or Sunday, keep moving to the next day
        while next_day.weekday() == 6 or cal.is_holiday(next_day): 
            next_day += timedelta(days=1)

        return next_day
                       
    def get_next_dates(self):
            daterow = [self.today]
            for _ in range(5):
                daterow.append(self.get_next_file_day(daterow[-1]))
                
            return daterow  
        
    def get_next_file_day(self,lastdate, filename="Personalplanung 2023.xlsx"):
            # Read the excel file using pandas
        df = pd.read_excel(filename, engine='openpyxl', header=None)
        
        # Find the column that matches the provided date by searching row 4 (Python uses 0-based indexing)
        matching_col_idx = None
        for idx, value in enumerate(df.iloc[3]):
            
            if isinstance(value, datetime):
                datevalue = value.date()
                
                if datevalue == lastdate:
                    matching_col_idx = idx + 1
                    return df.iloc[3][matching_col_idx].date()
                
        for idx, value in enumerate(df.iloc[3]):
            if isinstance(value, datetime):
                datevalue = value.date()
                
                if datevalue > date.today():
                    matching_col_idx = idx
                    return df.iloc[3][matching_col_idx].date()
                    
    
    def format_date_with_weekday(self, date_obj):
        # Dictionary for translating weekdays from English to German
        weekdays_translation = {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag"
        }

        english_weekday = date_obj.strftime("%A")
        german_weekday = weekdays_translation.get(english_weekday, english_weekday)
        return german_weekday + date_obj.strftime(" %Y-%m-%d")


