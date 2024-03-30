import tkinter as tk
import ttkbootstrap as ttk
from data_manager import TimeDataManager, DailyHoursManager
from atoms import TimeCaptureUnit, TimeFilledUnit
from datetime import time, timedelta

class TimeManager:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.framename = "Arbeitsbeginne"
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
        self.framename = "Arbeitsdauer"
        self.times_frame = ttk.Frame(self.frame)
        self.datamanager = DailyHoursManager()
        self.data = self.datamanager.read_hours()
        self.days = []
        if len(self.data) == 6:
            for dayset in self.data:
                day, duration = dayset
                self.days.append(FilledDayTimeAdjuster(self.times_frame, day, duration, self.refresh))
        else:
            days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"] 
            for day in days:
                self.days.append(FilledDayTimeAdjuster(self.times_frame, day, "8:00", self.refresh))
            
        for day in self.days:
            day.frame.pack(side="top", padx=16)
            
        self.times_frame.pack(side="top")
        self.total_frame = ttk.Frame(self.frame)
        self.total_label = ttk.Label(self.total_frame, text="Gesamt:", width=8)
        self.total_variable = tk.StringVar(value=self.total_time())
        self.total_time_label = ttk.Label(self.total_frame, textvariable=self.total_variable)
        self.total_label.pack(side="left", pady="8", padx="8")
        self.total_time_label.pack(side="left", padx="8",)
        self.separator = ttk.Separator(self.frame, orient='horizontal')
        
        self.save_frame = ttk.Frame(self.frame)
        self.save_button = ttk.Button(self.save_frame, text="Speichern", command=self.save)
        
        self.total_frame.pack(side="top", padx=8)
        self.separator.pack(side="top", fill="x", padx=16)
        self.save_button.pack(side="right", pady=16)
        self.save_frame.pack(side="right", padx=16)
        
    def return_data(self):
        timesets = []
        for item in self.days:
            timesets.append((item.day, item.duration_variable.get()))
        
        return timesets
            
    def total_time(self):
        # Initialize the total duration as 0
        total_duration = timedelta()
        # Sum all time durations
        for item in self.days:
            time_string = item.duration_variable.get()
            hours, minutes = map(int, time_string.split(":"))
            total_duration += timedelta(hours=hours, minutes=minutes)
        
        # Convert total_duration back to "HH:MM" format
        total_hours = total_duration.days * 24 + total_duration.seconds // 3600
        total_minutes = (total_duration.seconds % 3600) // 60
        
        return f"{total_hours:02d}:{total_minutes:02d}"
            
    def refresh(self):
        self.total_variable.set(self.total_time())
        
    def save(self):
        self.datamanager.save_hours(self.return_data())
        
        
class FilledDayTimeAdjuster:
    def __init__(self, master, day, time, refresh=None):
        self.master = master
        self.refresh = refresh
        self.frame = ttk.Frame(self.master)
        self.day = day
        self.duration_variable = tk.StringVar(value=time)
        self.day_label = ttk.Label(self.frame, text = day, width=12)
        self.duration_entry = ttk.Entry(self.frame, width="4", textvariable=self.duration_variable)
        self.day_label.pack(side="left", pady=16)
        self.duration_entry.pack(side="right")
        
        self.duration_entry.bind('<Return>', self.on_enter)
        self.duration_entry.bind('<FocusOut>', self.on_focus_out)


    def on_enter(self, *args):
        # This method is called whenever an entry's value changes.
        # Here, call the refresh method.
        self.refresh()
        self.duration_entry.master.focus_set()
        
    def on_focus_out(self, event):
        # This method is called when the widget loses focus.
        self.refresh()
        
    def return_data(self):
        return (self.day, self.duration_entry.get())

