# widgets.py
import tkinter as tk
from tkinter import ttk
from datetime import timedelta
from datetime import datetime
from atoms import ColorChangingButton
from data_manager import TimeManager
from data_manager import DailyHoursManager
from data_manager import get_next_working_day, format_date_with_weekday


class SideMenu:
    def __init__(self, master, width=200):
        self.master = master
        self.width = width
        self.buttons = []

        # Create the side menu frame
        self.frame = tk.Frame(master, width=self.width)
        self.frame.pack(side="left", fill="y", padx=(0, 10))

        # Add buttons
        self.add_button("Tagesplanung", self.open_tagesplanung)
        self.add_button("Zeiten", self.open_zeiten)
        self.add_button("Touren", self.open_touren)

    def add_button(self, text, command):
        button = ColorChangingButton(self.frame, text, command)
        self.buttons.append(button)

    def deactivate_other_buttons(self, except_button):
        for button in self.buttons:
            if button != except_button:
                button.deactivate_button()

    # Example functions for menu items
    def open_tagesplanung(self):
        self.deactivate_other_buttons(self.buttons[0])
        print("Tagesplanung selected")

    def open_zeiten(self):
        self.deactivate_other_buttons(self.buttons[1])
        print("Zeiten selected")

    def open_touren(self):
        self.deactivate_other_buttons(self.buttons[2])
        print("Touren selected")



class CombinedTimeSection:
    def __init__(self, master, start_times):
        self.master = master

        # Configure the style for the notebook tabs
        style = ttk.Style()
        style.configure("TNotebook.Tab", background="#D3D3D3", padding=[10, 4])  # Inactive tab color (grey)
        style.map("TNotebook.Tab", background=[("selected", "#ADD8E6")])  # Active tab color (light blue)

        # Create the main frame for this combined section
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True, pady=10)

        # Create Notebook widget
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True)

        # Add the DailyWorkingTimesSection and TimeEntrySection as tabs       
        self.time_entry_section = TimeEntrySection(self.notebook)
        self.notebook.add(self.time_entry_section.frame, text='Beginn')


        self.daily_working_times_section = DailyWorkingTimesSection(self.notebook, start_times)
        self.notebook.add(self.daily_working_times_section.frame, text='Arbeitszeiten')


        # Add a 'Save' button for both sections
        self.save_button = tk.Button(self.frame, text="Save", command=self.save_all, bg="#007aff", fg="white")
        self.save_button.pack(pady=10)

    def save_all(self):
        # Save data from both sections
        self.time_entry_section.save_times()
        self.daily_working_times_section.save_times()





class TimeEntrySection:
    def __init__(self, master):
        self.master = master

        # Create the frame for this section
        self.frame = tk.Frame(master, padx=32, pady=32)
        self.frame.pack(fill="x", pady=10)

        # Define the labels
        labels = ["1. Welle", "2. Welle", "Innendienst", "Spätschicht", "Pause"]

        # Create label and entry pairs using grid
        self.entries = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(self.frame, text=label_text)
            label.grid(row=i, column=0, sticky="e")

            entry = tk.Entry(self.frame, width=16)
            entry.grid(row=i, column=1, sticky="w")
            self.entries[label_text] = entry

        # Initialize data manager
        self.time_manager = TimeManager()
        self.load_times()


    def load_times(self):
        times = self.time_manager.read_times()
        for label, time in times.items():
            self.entries[label].delete(0,tk.END)
            self.entries[label].insert(0, time)

    def create_label_entry_pair(self, label_text):
        label = tk.Label(self.frame, text=label_text)
        label.pack(side="top", anchor="e")

        entry = tk.Entry(self.frame, width=6)  # Width adjusted to approximately 128 pixels
        entry.pack(side="top", anchor="e", padx=10)

        self.entries[label_text] = entry

    def save_times(self):
        new_times = {label: entry.get() for label, entry in self.entries.items()}
        self.time_manager.save_times(new_times)
        print("Times saved!")  # Optional: Confirmation message


class DailyWorkingTimesSection:
    def __init__(self, master, start_times):
        self.master = master
        self.start_times = start_times
        self.hours_manager = DailyHoursManager()

        # Create the frame for this section
        self.frame = tk.Frame(master, padx=32, pady=32)
        self.frame.pack(fill="x", pady=10)

        self.days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
        self.entries = {}
        self.end_time_labels_1 = {}  # For 1. Welle
        self.end_time_labels_2 = {}  # For 2. Welle
        
        # Define colors for alternating columns
        color1 = "#f0f0f0"  # Light grey
        color2 = "#e0e0e0"  # Slightly darker grey

        # Configure grid columns to have uniform spacing, plus an extra column for 'Calculate' and 'Total Time'
        for i in range(len(self.days) + 2):
            self.frame.grid_columnconfigure(i, weight=1)

        # Create labels for each day of the week
        for i, day in enumerate(self.days):
            tk.Label(self.frame, text=day).grid(row=0, column=i+1)

        # Create entry fields for each day
        for i, day in enumerate(self.days):
            entry = tk.Entry(self.frame, width=5)
            entry.grid(row=1, column=i+1)
            self.entries[day] = entry

        # Labels for "1. Welle" and "2. Welle" end times
        tk.Label(self.frame, text="1. Welle").grid(row=2, column=0)
        tk.Label(self.frame, text="2. Welle").grid(row=3, column=0)

        # Create UI elements and alternate background colors
        for i, day in enumerate(self.days):
            color = color1 if i % 2 == 0 else color2
            self.create_day_column(i + 1, day, color)
            

        # Place the 'Calculate' and 'Save' buttons, and 'Total Time' label in the same row
        self.calculate_button = tk.Button(self.frame, text="Feierabend berechnen", command=self.calculate_end_times,
                                          bg="light blue", fg="black")
        self.calculate_button.grid(row=1, column=len(self.days) + 1, padx=10, sticky="ew")

        # self.save_button = tk.Button(self.frame, text="Save", bg="#007aff", fg="white")
        # self.save_button.grid(row=2, column=len(self.days) + 1, padx=10, pady=10, sticky="ew")

        self.total_time_label = tk.Label(self.frame, text="Total Time: 00:00")
        self.total_time_label.grid(row=3, column=len(self.days) + 1, padx=10, sticky="ew")
        
        self.load_initial_times()
        
    def load_initial_times(self):
        hours_data = self.hours_manager.read_hours()
        for day, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, hours_data.get(day, ""))

        # Perform initial calculation of end times
        self.calculate_end_times()

    def save_times(self):
        new_hours = {day: entry.get() for day, entry in self.entries.items()}
        self.hours_manager.save_hours(new_hours)
        print("Times saved!")  # Optional: confirmation message


    def create_day_column(self, column, day, bg_color):
        # Day label
        tk.Label(self.frame, text=day, bg=bg_color).grid(row=0, column=column, sticky="ew")

        # Entry field
        entry = tk.Entry(self.frame, width=5)
        entry.grid(row=1, column=column, sticky="ew")
        self.entries[day] = entry

        # End time labels
        label_1 = tk.Label(self.frame, text="--:--", bg=bg_color)
        label_1.grid(row=2, column=column, sticky="ew")
        self.end_time_labels_1[day] = label_1

        label_2 = tk.Label(self.frame, text="--:--", bg=bg_color)
        label_2.grid(row=3, column=column, sticky="ew")
        self.end_time_labels_2[day] = label_2


    def calculate_end_times(self):
        # Fetch the latest start times and break time from TimeManager
        time_manager = TimeManager()
        current_start_times = time_manager.read_times()
        break_hours, break_minutes = map(int, current_start_times["Pause"].split(":"))
        break_duration = timedelta(hours=break_hours, minutes=break_minutes)

        total_time = timedelta()
        for day, entry in self.entries.items():
            try:
                hours, minutes = map(int, entry.get().split(":"))
                work_duration = timedelta(hours=hours, minutes=minutes) - break_duration

                # Calculating end times for both waves
                for wave in ["1. Welle", "2. Welle"]:
                    start_time_wave = timedelta(hours=int(current_start_times[wave].split(":")[0]), minutes=int(current_start_times[wave].split(":")[1]))
                    end_time = start_time_wave + work_duration
                    formatted_end_time = self.format_timedelta(end_time)
                    if wave == "1. Welle":
                        self.end_time_labels_1[day].config(text=str(formatted_end_time))
                    else:
                        self.end_time_labels_2[day].config(text=str(formatted_end_time))

                total_time += work_duration
            except ValueError:
                self.end_time_labels_1[day].config(text="Invalid")
                self.end_time_labels_2[day].config(text="Invalid")

        total_hours = total_time.total_seconds() / 3600
        formatted_total_time = f"{int(total_hours)}:{int((total_hours % 1) * 60):02d}"
        self.total_time_label.config(text=f"Gesamtarbeitszeit: {formatted_total_time} Stunden")

    def format_timedelta(self, td):
        """Format timedelta to hours and minutes."""
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours}:{minutes:02d}"

class WorkingDaysSection:
    def __init__(self, master):
        self.master = master

        # Configure the style for the notebook tabs
        style = ttk.Style()
        style.configure("TNotebook.Tab", background="#D3D3D3", padding=[10, 4])  # Inactive tab color (grey)
        style.map("TNotebook.Tab", background=[("selected", "#ADD8E6")])  # Active tab color (light blue)

        # Create the main frame for this section
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True, pady=10)

        # Create Notebook widget
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True)

        # Generate tabs for the next three working days
        current_day = datetime.now()
        for _ in range(3):
            current_day = get_next_working_day(current_day)
            formatted_day = format_date_with_weekday(current_day)
            day_frame = tk.Frame(self.notebook)
            self.notebook.add(day_frame, text=formatted_day)

