from datetime import date, timedelta, datetime
from workalendar.europe import Germany
import pandas as pd
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk
import pandas as pd

def create_gui():
    root = tk.Tk()
    root.title("Tour Selection")
    
    # To store the final DataFrame
    df_data = []

    # Function to toggle between 1.Welle and 2.Welle
    def toggle_wave(btn):
        current_text = btn["text"]
        btn["text"] = "2. Welle" if current_text == "1. Welle" else "1. Welle"

    # Function to save the selected data
    def save_and_exit():
        nonlocal df_data
        tour_data = []
        for i, (chk_var, switch_btn) in enumerate(widgets):
            if chk_var.get():
                tour_number = f"{i+1:03}"
                wave = switch_btn["text"]
                tour_data.append([tour_number, wave])
        
        df_data = pd.DataFrame(tour_data, columns=['Tour', 'Welle'])
        root.destroy()

    # Entry box for "Number of tours"
    ttk.Label(root, text="Number of tours:").pack(padx=5, pady=5)
    num_tours_var = tk.StringVar()
    num_tours_entry = ttk.Entry(root, textvariable=num_tours_var)
    num_tours_entry.pack(padx=5, pady=5)

    weiter_button = ttk.Button(root, text="Weiter", command=save_and_exit)
    weiter_button.pack(padx=5, pady=5, anchor=tk.NE)

    # Main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=5, pady=5)

    # Create two frames for the columns of tours
    left_frame = ttk.Frame(main_frame)
    right_frame = ttk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)
    right_frame.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)

    # A list to store widget references
    widgets = []

    def update_tours(*args):
        for frame in [left_frame, right_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        del widgets[:]

        try:
            n = int(num_tours_var.get())
            for i in range(n):
                frame = left_frame if i % 2 == 0 else right_frame

                # Checkbox
                cb_var = tk.BooleanVar(value=True)
                chk = ttk.Checkbutton(frame, variable=cb_var)
                chk.grid(row=i // 2, column=0, padx=5, pady=5)

                # Tour number label
                lbl = ttk.Label(frame, text=f"{i+1:03}")
                lbl.grid(row=i // 2, column=1, padx=5, pady=5)

                # Toggle button
                switch_btn = ttk.Button(frame, text="1. Welle", command=lambda btn=switch_btn: toggle_wave(btn))
                switch_btn.grid(row=i // 2, column=2, padx=5, pady=5)
                
                # Store the widget references
                widgets.append((cb_var, switch_btn))

        except ValueError:
            pass

    num_tours_var.trace_add("write", update_tours)
    root.mainloop()

    return df_data




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