import tkinter as tk
import ttkbootstrap as ttk
from data_manager import TimeManager
from atoms import TimeCaptureUnit, TimeFilledUnit

class TimeManager:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.datamanager = TimeManager()
        self.pairs = []
        for line in self.datamanager.read_times():
            job, time = line
            self.pairs.append(TimeFilledUnit(self.master, job, time))
            
        for pair in self.pairs:
            pair.pack()
        
            
   