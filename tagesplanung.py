from datetime import date, timedelta, datetime
from workalendar.europe import Germany
import pandas as pd
from interface import TourGui

def main():
    filename = "Personalplanung 2023.xlsx"
    gui = TourGui()
    gui.run()
    print(gui.dates)
    touren = gui.get_selected_tours()
    werktag = gui.get_next_working_day(date.today())
    data = learn_data_from_excel(filename=filename, desired_date=werktag)
    filtered = filter_df_by_selected_tours(data, touren)
    #print(data)
    
    
def filter_df_by_selected_tours(df, selected_tours):
    # Extract just the tour numbers from the selected tours ignoring the Welle
    selected_tour_numbers = [tour[0] for tour in selected_tours]

    # Filter the dataframe based on these tour numbers
    filtered_df = df[df['Stammtour'].isin(selected_tour_numbers)]
    print(df)
    print(filtered_df)
    return filtered_df


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