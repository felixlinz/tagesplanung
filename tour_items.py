import ttkbootstrap as ttk
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
        self.index = index
        self.parent = master_list
        self.tour_number = number
        self.frame = ttk.Frame(self.parent.frame, height="64", width= "256")
        self.tour_label = ttk.Label(self.frame, text=str(self.tour_number))
        # self.tour_label.config(font=("Myriad Pro", "44"))
        self.toggle_combo = ToggleEntryCombo(self.frame, int(wave)-1, alt_time )
        self.tour_label.pack(side="left")
        self.toggle_combo.frame.pack(side="left")
        
    def self_delete(self):
        self.parent.touren.remove(self)
                
        

