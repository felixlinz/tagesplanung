import tkinter as tk
import ttkbootstrap as ttk
from datetime import date 
from tour_items import TagesplanungTourList, EntryTourItem2
from data_manager import learn_data_from_excel, get_next_file_day
from data_manager import sort_workers, DailyToursManager
    
class TagesplanungEditor:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.framename = "Tagesplanung"
        self.working_days = self.get_working_days()

        self.notebook = ttk.Notebook(self.frame, style="journal")
        self.notebook.pack(fill="both", expand=True)
        day_configs = {}

        # Initialize DayConfig for each day and create a tab
        for day in self.working_days:
            day_string = str(day)
            day_frame = ttk.Frame(self.notebook)
            self.notebook.add(day_frame, text=day_string)
            day_configs[day] = TagesplanungDayTab(day_frame, day)
            
    def get_working_days(self):
        days = []
        days.append(get_next_file_day(date.today()))
        for _ in range(2):
            days.append(get_next_file_day(days[-1]))
        return days

    
class TagesplanungDayTab:
    def __init__(self, master, day):
        self.master = master
        self.day = day
        self.uberframe = ttk.Frame(master)
        self.frame = ttk.Frame(self.uberframe, borderwidth=1, relief="solid")
        self.day_data = learn_data_from_excel(day)
        self.data = sort_workers(self.day_data)
        self.day_tours_manager = DailyToursManager()
        self.day_tours = self.day_tours_manager.read_data(str(self.day))


        # Create a Canvas for the scrolling area
        self.canvas = tk.Canvas(self.frame, width = 322, height=556)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.tourlist = TagesplanungTourList(self.scrollable_frame, self.day_tours, self.data)
        if len(self.tourlist.touren) >= 1:
            self.tourlist.frame.pack(side="top")
        
        # Packing the Canvas and Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Save and Controls frames that stay fixed
        self.controls_frame = self.controls()
        self.save_frame = self.saveframe()
        self.frame.pack(side="top", pady="8")
        self.controls_frame.pack(side="top", fill="x", expand=True, pady="8")
        self.save_frame.pack(side="top", fill="x", pady="8")
        self.uberframe.pack(pady="8")

    def saveframe(self):
        save_frame = ttk.Frame(self.uberframe)
        self.save_button = ttk.Button(save_frame, text="Speichern", command=self.save)
        self.save_button.pack(side="right", anchor="w")
        return save_frame
    
    def save(self):
        self.datamanager.save_data(self.tourlist.get_updated_values(), self.day)   

    def controls(self):
        controls_frame = ttk.Frame(self.uberframe, height=128)
        controls_frame.pack_propagate(False)
        self.add_button = ttk.Button(controls_frame, text="+", command=self.query_extra_tour)
        self.add_button.pack(pady=16)
        return controls_frame

        
    def query_extra_tour(self):
        self.add_button.pack_forget()
        entry_item = EntryTourItem2(self.controls_frame, command=self.add_tour, number= self.get_number())
        entry_item.uberframe.pack(side="top")
        
    def get_number(self):
        try:
            return "{:03}".format(int(self.tourlist.touren[-1].tour_number) + 1)
        except IndexError:
            return "001"
        
    def add_tour(self, dataset):
        tour_number, wave, alt_time, item = dataset
        item.uberframe.destroy()
        self.tourlist.add_tour(tour_number, wave, alt_time)
        self.add_button.pack(pady=16)