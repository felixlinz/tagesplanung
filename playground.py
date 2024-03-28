# import tkinter as tk
from datetime import datetime
from datetime import date
import pandas as pd
import ttkbootstrap as ttk
from data_manager import learn_data_from_excel, sort_workers, DailyToursManager
from tour_items import TagesplanungTourList

date_string = "2023-03-28"  # Your date string here
date_format = "%Y-%m-%d"  # The format of your date string

date_obj = datetime.strptime(date_string, date_format).date()

dfs = sort_workers(learn_data_from_excel(date.today()))

master = ttk.Frame()
datamanager = DailyToursManager()
day_data = datamanager.read_data("tuesday")
dataeditor = TagesplanungTourList(master, day_data, dfs)
dataeditor.frame.pack()
master.pack()
master.mainloop()


"""print("Stammfahrer")
print(dfs["Stammfahrer"])
print("Springer")
print(dfs["Springer"])
print("Firmen")
print(dfs["Firmen"])
print("Einweisung")
print(dfs["Einweisung"])
print("Abrufer")
print(dfs["Abrufer"])"""

