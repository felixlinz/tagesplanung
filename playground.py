import tkinter as tk
import ttkbootstrap as ttk
from tour_items import TourItem
from data_manager import DailyToursManager

tourlist1 = [
 ('001', 1, ''),
 ('002', 3, '18:59'),
 ('003', 1, ''),
 ('004', 1, ''),
 ('005', 3, '10:48'),
 ('006', 3, '02:32'),
 ('007', 3, '12:22'),
 ('008', 3, '07:59'),
 ('009', 2, ''),
 ('010', 1, ''),
 ('011', 1, ''),
 ('012', 2, ''),
 ('013', 3, '04:35'),
 ('014', 2, ''),
 ('015', 1, ''),
 ('016', 3, '11:01'),
 ('017', 3, '02:55'),
 ('018', 1, ''),
 ('019', 3, '21:49'),
 ('020', 3, '09:59')
]

tourlist2 = [("001", 3, "09:59")]

class TourList:
    def __init__(self, master, list):
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

def print_values():
    datamanager.save_data(tour_list.get_updated_values(), weekday="dienstag")
    for item in tour_list.get_updated_values():
        print(item)
    


window = ttk.Frame()
datamanager = DailyToursManager()
tourlist = datamanager.read_data("Dienstag")
button = ttk.Button(window, text="return", command=print_values)
button.pack()
tour_list = TourList(window, tourlist)
tour_list.frame.pack()
window.pack()
window.mainloop()