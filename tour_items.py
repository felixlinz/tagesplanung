import ttkbootstrap as ttk
import tkinter as tk
from atoms import ToggleButton2, OptionalEntry

class ToggleEntryCombo:
    def __init__(self, master, wave_index, alt_time, grandparent=None):
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
    def __init__(self, master_list, number, wave, alt_time, grandparent = None):
        self.grandparent = grandparent
        self.uberframe = ttk.Frame(master_list.frame)
        self.parent = master_list
        self.tour_number = number
        self.frame = ttk.Frame(self.uberframe, height="64", width= "256")
        self.tour_label = ttk.Label(self.frame, text=str(self.tour_number))
        self.delete_button = ttk.Button(self.frame, text="x", width="1", command=self.self_delete)
        self.tour_label.config(font=("Myriad Pro", "18"))
        self.toggle_combo = ToggleEntryCombo(self.frame, int(wave)-1, alt_time )
        self.tour_label.pack(side="left", pady="4", padx="8")
        self.toggle_combo.frame.pack(side="left", pady="4", padx="8")
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
                
        
class EntryTourItem:
    def __init__(self, master, command, number ="001"):
        self.command = command
        self.uberframe = ttk.Frame(master)
        self.frame = ttk.Frame(self.uberframe, height="64", width= "256")
        self.tour_number_variable = tk.StringVar(value=number)
        self.tour_number = ttk.Entry(self.frame, width="3", textvariable=self.tour_number_variable)
        self.tour_number.config(font=("Myriad Pro", "12"))
        self.add_button = ttk.Button(self.frame, text=u"\u2713", command=lambda: self.command(self.return_values()))
        self.toggle_combo = ToggleEntryCombo(self.frame, 0, "00:00" )   
        self.tour_number.pack(side="left", pady="12")
        self.toggle_combo.frame.pack(side="left", pady="12")
        self.frame.pack(side="top", padx="16")
        self.add_button.pack(side="left", padx="8")
        separator = ttk.Separator(self.uberframe, orient='horizontal')
        separator.pack(side="bottom", fill='x')
        
        
    def self_add(self):
        if self.toggle_combo.toggle_button.return_state() == 2:
            alt_time = self.toggle_combo.alt_time
        else:
            alt_time = ""
        self.list.touren.add(TourItem(self.list, self.tour_number.get(), self.toggle_combo.return_state() + 1, alt_time))
        self.uberframe.destroy()
        
        
    def return_values(self):
        wave = self.toggle_combo.return_state() + 1
        if self.toggle_combo.toggle_button.return_state() == 2:
            alt_time = self.toggle_combo.alt_time
        else:
            alt_time = ""
        return (self.tour_number.get(), self.toggle_combo.return_state() +1, alt_time, self)   
                
                
class EntryTourItem2:
    def __init__(self, master, command, number ="001"):
        self.command = command
        self.uberframe = ttk.Frame(master)
        self.frame = ttk.Frame(self.uberframe, height="64", width= "256")
        self.tour_number_variable = tk.StringVar(value=number)
        self.tour_number = ttk.Entry(self.frame, width="3", textvariable=self.tour_number_variable)
        self.tour_number.config(font=("Myriad Pro", "12"))
        self.add_button = ttk.Button(self.frame, text=u"\u2713", command=lambda: self.command(self.return_values()))
        self.toggle_combo = ToggleEntryCombo(self.frame, 0, "00:00" )   
        self.tour_number.pack(side="left", pady="12")
        self.toggle_combo.frame.pack(side="left", pady="12")
        self.frame.pack(side="top", padx="16")
        self.add_button.pack(side="left", padx="8")
        separator = ttk.Separator(self.uberframe, orient='horizontal')
        separator.pack(side="bottom", fill='x')
        
        
    def self_add(self):
        if self.toggle_combo.toggle_button.return_state() == 2:
            alt_time = self.toggle_combo.alt_time
        else:
            alt_time = ""
        self.list.touren.add(TourItem(self.list, self.tour_number.get(), self.toggle_combo.return_state() + 1, alt_time))
        self.uberframe.destroy()
        
        
    def return_values(self):
        wave = self.toggle_combo.return_state() + 1
        if self.toggle_combo.toggle_button.return_state() == 2:
            alt_time = self.toggle_combo.alt_time
        else:
            alt_time = ""
        return (self.tour_number.get(), self.toggle_combo.return_state() +1, alt_time, self)   
                
class TourList:
    def __init__(self, master, tourlist):
        self.frame = ttk.Frame(master, height="400")      
        self.touren = []
        
        for n, dataset in enumerate(tourlist):
            tour_number, wave_number, alt_time = dataset
            item = TourItem(self, tour_number, wave_number, alt_time)
            self.touren.append(item)
        
        self.refresh()
        
    def refresh(self):
        self.touren.sort(key=lambda x: int(x.tour_number))
        for item in self.touren:
            item.uberframe.pack(side="top")
            
            
    def get_updated_values(self):
        updated_list = []
        for item in self.touren:
            updated_list.append(item.return_values())
        return updated_list
        

class TourList2:
    def __init__(self, master, tourlist, grandparent=None, parent=None):
        self.grandparent = grandparent
        self.parent = None
        self.frame = tk.Canvas(master, height="400")    
        self.touren = []
        self.tour_numbers = set()
        
        for dataset in tourlist:
            tour_number, wave_number, alt_time = dataset
            item = TourItem(self, tour_number, wave_number, alt_time)
            self.tour_numbers.add(int(tour_number))
            self.touren.append(item)
        
        for item in self.touren:
            item.uberframe.pack(side="top")
        
        self.refresh()
              
    def refresh(self):
        # Sort the list first
        self.touren.sort(key=lambda x: int(x.tour_number))
        
        # Remove duplicates: Create a new list without duplicates
        unique_touren = []
        seen_numbers = set()
        for item in self.touren:
            if item.tour_number not in seen_numbers:
                unique_touren.append(item)
                seen_numbers.add(item.tour_number)
        
        # Now unique_touren has all unique items, sorted by tour_number
        self.touren = unique_touren
        
        # Clear the existing items from the GUI
        for item in self.frame.winfo_children():
            item.pack_forget()
        
        # Repack the items in self.touren
        for item in self.touren:
            item.uberframe.pack(side="top")
            
        self.frame.configure(scrollregion=self.frame.bbox("all"))
        if self.parent:
            self.parent.canvas.configure(scrollregion=self.parent.canvas.bbox("all"))


            
    def add_tour(self, tour_number, wave, alt_time):
        if tour_number not in self.tour_numbers:
            if int(tour_number) > max(self.tour_numbers):
                self.touren.append(TourItem(self, tour_number, wave, alt_time))
                self.refresh()
            else:
                self.touren.sort(key=lambda x: int(x.tour_number))
                self.touren[-1].uberframe.pack(side="top")
                
    def get_updated_values(self):
        updated_list = []
        for item in self.touren:
            updated_list.append(item.return_values())
        return updated_list
                    
    
                
class TagesplanungTourList:
    def __init__(self, master, tourlist, tagesplanung):
        """
        dataframe relevant  info not working
        
        """
        self.tourlist = tourlist # [(tourstring, wave, alt_time)]
        self.tagesplanung = tagesplanung
        self.stammfahrer = self.tagesplanung["Stammfahrer"]
        self.springer = self.tagesplanung["Springer"]
        self.used_names = set()
        self.abrufer = self.tagesplanung["Abrufer"]
        self.firmenzusteller = self.tagesplanung["Firmen"]
        self.Einweisung = self.tagesplanung["Einweisung"]
        self.frame = tk.Canvas(master, height="400")      
        self.touren = []
        self.tour_numbers = set()
        
        for dataset in self.tourlist:
            tour_number, wave_number, alt_time = dataset
            filtered_df = self.stammfahrer[self.stammfahrer['Stammtour'] == int(tour_number)]
            if not filtered_df.empty:
                driver_name = filtered_df["Name"].iloc[0]
            else:
                if name := self.get_unused_name(self.springer):
                    driver_name = name
                else:
                    if name := self.get_unused_name(self.abrufer):
                        driver_name = name
                        
            item = DriverTourItem(self, driver_name, tour_number, wave_number, alt_time)
            self.tour_numbers.add(int(tour_number))
            self.touren.append(item)
        
        for item in self.touren:
            item.uberframe.pack(side="top")
        
        self.refresh()
        
    def get_unused_name(self, df):
        """
        Selects an unused name from the given DataFrame.

        Args:
        df (pd.DataFrame): The DataFrame to select the name from.

        Returns:
        str or None: Returns a name that hasn't been used yet, or None if no unused names are available.
        """
        # Filter the DataFrame to only include names that haven't been used yet
        available_names = df[~df['Name'].isin(self.used_names)]['Name']

        if not available_names.empty:
            # If there are available names, select the first one
            name_value = available_names.iloc[0]
            # Mark this name as used by adding it to the set
            self.used_names.add(name_value)
            return name_value
        else:
            # Return None if no unused names are available
            return None
              
    def refresh(self):
        # Sort the list first
        self.touren.sort(key=lambda x: int(x.tour_number))
        
        # Remove duplicates: Create a new list without duplicates
        unique_touren = []
        seen_numbers = set()
        for item in self.touren:
            if item.tour_number not in seen_numbers:
                unique_touren.append(item)
                seen_numbers.add(item.tour_number)
        
        # Now unique_touren has all unique items, sorted by tour_number
        self.touren = unique_touren
        
        # Clear the existing items from the GUI
        for item in self.frame.winfo_children():
            item.pack_forget()
        
        # Repack the items in self.touren
        for item in self.touren:
            item.uberframe.pack(side="top")
            
    def add_tour(self, tour_number, wave, alt_time):
        if tour_number not in self.tour_numbers:
            if int(tour_number) > max(self.tour_numbers):
                self.touren.append(TourItem(self, tour_number, wave, alt_time))
                self.refresh()
            else:
                self.touren.sort(key=lambda x: int(x.tour_number))
                self.touren[-1].uberframe.pack(side="top")
                
        
            
    def get_updated_values(self):
        updated_list = []
        for item in self.touren:
            updated_list.append(item.return_values())
        return updated_list
    
    
class DriverTourItem:
    def __init__(self, master_list, driver, number, wave, alt_time = ""):
        self.uberframe = ttk.Frame(master_list.frame)
        self.parent = master_list
        self.driver = driver
        self.tour_number = number
        self.frame = ttk.Frame(self.uberframe, height="64", width= "256")
        self.tour_label = ttk.Label(self.frame, text=str(self.tour_number))
        self.driver_variable = tk.StringVar(value=self.driver)
        self.driver_entry = ttk.Entry(self.frame, textvariable=self.driver_variable, width="8")
        self.delete_button = ttk.Button(self.frame, text="x", width="1", command=self.self_delete)
        self.tour_label.config(font=("Myriad Pro", "18"))
        self.toggle_combo = ToggleEntryCombo(self.frame, int(wave)-1, alt_time )
        self.tour_label.pack(side="left", pady="4", padx="8")
        self.driver_entry.pack(side="left", pady="4", padx="8")
        self.toggle_combo.frame.pack(side="left", pady="4", padx="8")
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
        return (self.tour_number,self.driver_variable.get(), wave, alt_time)