# import tkinter as tk
import ttkbootstrap as ttk
from tour_items import TourItem, TourList
from data_manager import DailyToursManager

window = ttk.Frame()
datamanager = DailyToursManager()

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)
day_configs = {}

# Days of the week in German (excluding Sunday)
days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]

# Initialize DayConfig for each day and create a tab
for day in days:
    day_frame = ttk.Frame(notebook)
    notebook.add(day_frame, text=day)
    day_configs[day] = TourList(day_frame, datamanager.read_data("dienstag"))
            
window.pack()
window.mainloop()