# import tkinter as tk
import ttkbootstrap as ttk
from times_manager import DailyTimesManager, FilledDayTimeAdjuster


master = ttk.Frame()
datamanager = DailyTimesManager(master)
datamanager.frame.pack()
master.pack()
master.mainloop()
