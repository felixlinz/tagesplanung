# import tkinter as tk
import ttkbootstrap as ttk
from times_manager import TimeManager


master = ttk.Frame()
datamanager = TimeManager(master=master)
datamanager.frame.pack()
master.mainloop()