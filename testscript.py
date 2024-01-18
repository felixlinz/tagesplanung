from data_manager import get_next_working_day
from data_manager import format_date_with_weekday
from data_manager import learn_data_from_excel
from data_manager import sort_workers
from datetime import datetime, date
import pandas as pd
import tkinter



# Example usage
root = tk.Tk()
tage_konfigurieren = TageKonfigurieren(root)
root.mainloop()
# sorted_numeric, sorted_s, sorted_df = sort_workers(df)
# print("Numeric Stammtour and Einsatz = 1:")
# print(sorted_numeric)
# print("\nStammtour = 's' and Einsatz = 1:")
# print(sorted_s)
# print("\nEinsatz = 'df':")
# print(sorted_df)
# print("Numeric Stammtour and Einsatz = 1:")
# print(sorted_numeric)
# print("\nStammtour = 's' and Einsatz = 1:")
# print(sorted_s)