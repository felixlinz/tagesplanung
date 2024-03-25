import ttkbootstrap as ttk
import tkinter as tk
from atoms import ToggleButton2, OptionalEntry

class ToggleEntryCombo:
    def __init__(self, master, wave_index, alt_time):
        self.frame = ttk.Frame(master)
        self.alt_time = alt_time
        self.toggle_button = ToggleButton2(self.frame, ["1", "2", "?"], command=self.activate_entry, command_button_index=2)
        self.entry = OptionalEntry(self.frame, entry_value = self.alt_time)
        self.toggle_button.set_active_button(wave_index)
        self.toggle_button.frame.pack(side="left", padx="8", pady="8")
        self.entry.frame.pack(side="left", padx=8)
                
    def activate_entry(self, state):
        if state == True:
            self.entry.activate()
        else:
            self.entry.deactivate()
            
    def return_state(self):
        self.alt_time = self.entry.get()
        return self.toggle_button.return_state()
            
        

class TourItem:
    def __init__(self, master_list, number, wave, alt_time, index):
        self.uberframe = ttk.Frame(master_list.frame)
        self.index = index
        self.parent = master_list
        self.tour_number = number
        self.frame = ttk.Frame(self.uberframe, height="64", width= "256")
        self.tour_label = ttk.Label(self.frame, text=str(self.tour_number))
        self.delete_button = ttk.Button(self.frame, text="x", command=self.self_delete)
        self.tour_label.config(font=("Myriad Pro", "18"))
        self.toggle_combo = ToggleEntryCombo(self.frame, int(wave)-1, alt_time )
        self.tour_label.pack(side="left", pady="12")
        self.toggle_combo.frame.pack(side="left", pady="12")
        self.delete_button.pack(side="left", padx="4")
        self.frame.pack(side="top", padx="16")
        separator = ttk.Separator(self.uberframe, orient='horizontal')
        separator.pack(side="bottom", fill='x')
        
    def self_delete(self):
        self.parent.touren.remove(self)
        self.uberframe.destroy()
        
    def return_values(self):
        wave = self.toggle_combo.return_state() + 1
        if self.toggle_combo.toggle_button.return_state() == 2:
            alt_time = self.toggle_combo.alt_time
        else:
            alt_time = ""
        return (self.tour_number, wave, alt_time)
                
                
class TourList:
    def __init__(self, master, tourlist):
        self.frame = ttk.Frame(master, height="400")      
        self.touren = []
        
        for n, dataset in enumerate(tourlist):
            tour_number, wave_number, alt_time = dataset
            item = TourItem(self, tour_number, wave_number, alt_time, n)
            self.touren.append(item)
        
        for item in self.touren:
            item.uberframe.pack(side="top")
            
    def get_updated_values(self):
        updated_list = []
        for item in self.touren:
            updated_list.append(item.return_values())
        return updated_list
        

