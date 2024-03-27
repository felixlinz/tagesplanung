import tkinter as tk
import ttkbootstrap as ttk
from data_manager import TimeDataManager, DailyHoursManager
from atoms import TimeCaptureUnit, TimeFilledUnit
from datetime import time, timedelta

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
        return values
            
    def add(self):
        self.pairs.append(TimeCaptureUnit(self.master, delete_function=self.delete))
        self.pairs[-1].frame.pack(side="top",pady="8", padx="16")
        
    def delete(self, item):
        item.frame.pack_forget()
        self.pairs.remove(item)
        
        
class DailyTimesManager:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.datamanager = DailyHoursManager()
        self.data = self.datamanager.read_hours()
        self.days = []
        for dayset in self.data:
            day, duration = dayset
            self.days.append(FilledDayTimeAdjuster(self.frame, day, duration, self.refresh))
        for day in self.days:
            day.frame.pack(side="top")
            
        self.total_frame = ttk.Frame(self.master)
        self.total_label = ttk.Label(self.total_frame, text="Gesamt:")
        self.total_variable = tk.StringVar(value=self.total_time())
        self.total_time_label = ttk.Label(self.total_frame, textvariable=self.total_variable)
        self.total_label.pack(side="left", pady="8", padx="8")
        self.total_time_label.pack(side="left", padx="8")
        self.total_frame.pack(side="bottom")
        
        
    def total_time(self):
        # Initialize the total duration as 0
        total_duration = timedelta()
        # Sum all time durations
        for item in self.days:
            time_string = item.time
            hours, minutes = map(int, time_string.split(":"))
            total_duration += timedelta(hours=hours, minutes=minutes)
        
        # Convert total_duration back to "HH:MM" format
        total_hours = total_duration.days * 24 + total_duration.seconds // 3600
        total_minutes = (total_duration.seconds % 3600) // 60
        
        return f"{total_hours:02d}:{total_minutes:02d}"
            
    def refresh(self):
        self.total_variable = self.total_time()
        
        
class FilledDayTimeAdjuster:
    def __init__(self, master, day, time, refresh=None):
        self.master = master
        self.refresh = refresh
        self.frame = ttk.Frame(self.master)
        self.day = day
        self.time = time
        self.duration_variable = tk.StringVar(value=time)
        self.day_label = ttk.Label(self.master, text = day)
        self.duration_entry = ttk.Entry(self.master, width="4", textvariable=self.duration_variable)
        self.day_label.pack(side="left", pady=16)
        self.duration_entry.pack(side="left")
        
        self.duration_entry.bind('<Return>', self.on_enter)

    def on_enter(self, *args):
        # This method is called whenever an entry's value changes.
        # Here, call the refresh method.
        self.refresh()
        
    def return_data(self):
        return (self.day, self.duration_entry.get())

