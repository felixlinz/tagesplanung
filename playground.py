# import tkinter as tk
from datetime import datetime
from datetime import date
import pandas as pd
import ttkbootstrap as ttk
from data_manager import learn_data_from_excel, sort_workers, DailyToursManager, get_next_file_day
from tour_items import TagesplanungTourList
from touren_manager import DaysEditor
from tagesplanungs_manager import TagesplanungEditor
from widgets import SideMenu

from data_manager import PathManager

master = ttk.Frame()

konfiguration = DaysEditor(master)
tagesplanung = TagesplanungEditor(master)
konfiguration.frame.pack(side="left")
tagesplanung.frame.pack(side="left")
master.pack()

master.mainloop()