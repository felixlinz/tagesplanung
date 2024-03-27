# widgets.py
import tkinter as tk
from tkinter import ttk
from datetime import timedelta
from datetime import datetime
from atoms import ColorChangingButton, TourItem, TourItemCreator, ColorChangingButton2
from data_manager import TimeDataManager
from data_manager import DailyHoursManager
from data_manager import get_next_working_day, format_date_with_weekday


class SideMenu:
    def __init__(self, master, width=200):
        self.master = master
        self.width = width
        self.buttons = []
        self.frames = {}
        self.current_frame = None

        # Create the side menu frame
        self.frame = tk.Frame(master, width=self.width)
        self.frame.pack(side="left", fill="y", padx=(8, 8))
        
        self.init_frames()

        # Add buttons
        self.add_button("Tagesplanung", command=lambda: self.switch_frame(NextDaysPlan))
        self.add_button("Zeiten", command=lambda: self.switch_frame(KombinierteZeitKonfiguration))
        self.add_button("Touren", command=lambda: self.switch_frame(TourenKonfiguration))

        
        for button in self.buttons:
            button.add_other_buttons(self.buttons)
            
        self.buttons[0].activate_button()
        self.switch_frame(NextDaysPlan)
        
    def switch_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.frame.pack_forget()  # Hide the current frame

        # Retrieve the frame instance from the dictionary
        self.current_frame = self.frames[frame_class]
        self.current_frame.frame.pack(fill="both", expand=True, pady=10)  # Show the frame

    def add_button(self, text, command):
        button = ColorChangingButton2(self, text, command=command)
        self.buttons.append(button)

    def init_frames(self):
        # Create instances of all frames here and store them
        self.frames[TourenKonfiguration] = TourenKonfiguration(self.master)        
        self.frames[NextDaysPlan] = NextDaysPlan(self.master)
        self.frames[KombinierteZeitKonfiguration] = KombinierteZeitKonfiguration(self.master)#
        # self.frames[TourenKonfiguration] = TourenKonfiguration(self.master)




class KombinierteZeitKonfiguration:
    def __init__(self, master):
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
        self.time_entry_section = StartzeitKonfiguration(self.notebook)
        self.notebook.add(self.time_entry_section.frame, text='Beginn')


        self.daily_working_times_section = TagesRegelzeitKonfigurtion(self.notebook)
        self.notebook.add(self.daily_working_times_section.frame, text='Arbeitszeiten')


        # Add a 'Save' button for both sections
        self.save_button = tk.Button(self.frame, text="Save", command=self.save_all, bg="#007aff", fg="white")
        self.save_button.pack(pady=10)

    def save_all(self):
        # Save data from both sections
        self.time_entry_section.save_times()
        self.daily_working_times_section.save_times()





class StartzeitKonfiguration:
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


class TagesRegelzeitKonfigurtion:
    def __init__(self, master):
        self.master = master
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


class NextDaysPlan:
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


class TourenKonfiguration:
    """
    Manages the overall configuration of tours for different days of the week.

    Attributes:
    - master (Tk widget): The parent Tk widget.
    - day_configs (dict): A dictionary to keep track of DayConfig instances for each day.
    - notebook (ttk.Notebook): A notebook widget to create tabs for each day.
    """
    def __init__(self, master):
        self.master = master
        self.day_configs = {}  # Dictionary to keep track of DayConfig instances for each day

        # Create Notebook widget
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)

        # Days of the week in German (excluding Sunday)
        days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]

        # Initialize DayConfig for each day and create a tab
        for day in days:
            day_frame = tk.Frame(self.notebook)
            self.notebook.add(day_frame, text=day)
            self.day_configs[day] = DayConfig(day_frame, day)
            
        
class DayConfig:
    def __init__(self, parent_frame, day):
        self.parent_frame = parent_frame
        self.day = day
        self.touren_amount = 20
        self.tk_touren_amount = tk.IntVar(value=self.touren_amount)
        self.frame = self.initialize_frame()
        self.touren = self.generate_tour_items()
        self.frame.pack(fill="both", expand=True)

    def initialize_frame(self):
        frame = tk.Frame(self.parent_frame, width=600, height=400)
        self.create_controls()
        self.create_tour_display_area()
        
        return frame

    def create_controls(self):
        """
        Creates increment and decrement buttons, and an edit field for touren_amount.
        """
        increment_button = tk.Button(self.frame, text="+", command=self.increment_touren)
        increment_button.pack(side="left")

        edit_field = tk.Entry(self.frame, textvariable=self.tk_touren_amount)
        edit_field.pack(side="left")

        decrement_button = tk.Button(self.frame, text="-", command=self.decrement_touren)
        decrement_button.pack(side="left")

    def create_tour_display_area(self):
        # Create a scrollable area for tours
        self.scrollable_frame = tk.Frame(self.frame)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.tours_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.tours_frame, anchor="nw")

    def increment_touren(self):
        self.tk_touren_amount.set(self.tk_touren_amount.get() + 1)
        self.refresh_tour_items()

    def decrement_touren(self, number=None):
        new_value = max(0, self.tk_touren_amount.get() - 1)
        self.tk_touren_amount.set(new_value)
        if number is not None:
            self.touren = [tour for tour in self.touren if tour.number != number]
        self.refresh_tour_items()

    def generate_tour_items(self):
        self.clear_tour_items()
        for i in range(self.tk_touren_amount.get()):
            TourItem(self.tours_frame, i+1, time="1.", delete_callback=self.decrement_touren)

    def refresh_tour_items(self):
        self.generate_tour_items()

    def clear_tour_items(self):
        for widget in self.tours_frame.winfo_children():
            widget.destroy()

    def update_touren_amount_from_entry(self):
        # This method can be called to update `touren_amount` based on the Entry widget, if needed
        self.touren_amount = self.tk_touren_amount.get()
        self.refresh_tour_items()