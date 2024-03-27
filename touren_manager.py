class DaysEditor:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.datamanager = DailyToursManager()

        self.notebook = ttk.Notebook(self.frame, style="journal")
        self.notebook.pack(fill="both", expand=True)
        day_configs = {}

        # Days of the week in German (excluding Sunday)
        days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]

        # Initialize DayConfig for each day and create a tab
        for day in days:
            day_frame = ttk.Frame(self.notebook)
            self.notebook.add(day_frame, text=day)
            day_configs[day] = DayTab(day_frame, day, self.datamanager)


class DayTab:
    def __init__(self, master, day, datamanager):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.day = day
        self.datamanager = datamanager
        self.data = self.datamanager.read_data(day)
        self.tourlist = TourList2(self.master, self.data)
        self.controls_frame = self.controls(self.frame)
        self.save_frame = self.saveframe(self.frame)
        self.controls_frame.pack(side="top", fill="x", expand = "True", pady="8")
        if len(self.tourlist.touren) >= 1:
            self.tourlist.frame.pack(side="top")
        self.save_frame.pack(side="bottom", pady="8")
        self.frame.pack()
        
    def saveframe(self, master):
        save_frame = ttk.Frame(master)
        self.save_button = ttk.Button(save_frame, text="Speichern", command=self.save)
        self.save_button.pack(side="left")
        
        return save_frame
        
    def save(self):
        self.datamanager.save_data(self.tourlist.get_updated_values(), self.day)    
        
    def controls(self, master):
        controls_frame = ttk.Frame(master)
        self.add_button = ttk.Button(controls_frame, text="+", command=self.query_extra_tour)
        self.add_button.pack()
        
        return controls_frame
        
    def query_extra_tour(self):
        self.add_button.pack_forget()
        entry_item = EntryTourItem(self.controls_frame, command=self.add_tour, number= self.get_number())
        entry_item.uberframe.pack(side="left")
        
    def get_number(self):
        try:
            return "{:03}".format(int(self.tourlist.touren[-1].tour_number) + 1)
        except IndexError:
            return "001"
        
    def add_tour(self, dataset):
        tour_number, wave, alt_time, item = dataset
        item.uberframe.destroy()
        self.tourlist.add_tour(tour_number, wave, alt_time)
        self.add_button.pack()