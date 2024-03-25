from data_manager import get_next_working_day
from data_manager import format_date_with_weekday
from data_manager import learn_data_from_excel
from data_manager import sort_workers
from atoms import ColorChangingButton2, ToggleButton
from widgets import SideMenu, NextDaysPlan, TagesRegelzeitKonfigurtion, TourenKonfiguration
from datetime import datetime, date
import pandas as pd
import tkinter as tk



def main():
    root = tk.Tk()
    SideMenu(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()