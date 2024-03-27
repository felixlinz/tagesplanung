import tkinter as tk
import ttkbootstrap as ttk
from data_manager import TimeDataManager
from atoms import TimeCaptureUnit, TimeFilledUnit

class TimeManager:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.datamanager = TimeDataManager()
        self.pairs = []
        for line in self.datamanager.read_times():
            job, time = line
            if job != "":
                self.pairs.append(TimeFilledUnit(self.master, job, time, delete_function=self.delete))
            
        for pair in self.pairs:
            pair.frame.pack(side="top", pady="8", padx="16")
            
        self.addbutton = ttk.Button(self.master, text="+", command=self.add)
        self.saveframe = ttk.Frame(self.master)
        self.savebutton = ttk.Button(self.saveframe, text="Speichern", command=self.save)
        self.savebutton.pack(side="right", pady=8, padx=8)
        self.saveframe.pack(side="bottom")
        self.addbutton.pack(side="bottom", pady=8)
        
    def save(self):
        self.datamanager.save_times(self.return_values())
        
    def return_values(self):
        values = []
        for pair in self.pairs:
            values.append(pair.values())
        print(values)
        return values
            
    def add(self):
        self.pairs.append(TimeCaptureUnit(self.master, delete_function=self.delete))
        self.pairs[-1].frame.pack(side="top",pady="8", padx="16")
        
    def delete(self, item):
        item.frame.pack_forget()
        self.pairs.remove(item)