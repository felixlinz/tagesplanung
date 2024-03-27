# import tkinter as tk
import ttkbootstrap as ttk
from times_manager import TimeManager


master = ttk.Frame()
datamanager = TimeManager(master)
datamanager.frame.pack(fill="both", expand=True, pady=8)
master.pack()
master.mainloop()
