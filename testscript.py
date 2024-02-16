from data_manager import get_next_working_day
from data_manager import format_date_with_weekday
from data_manager import learn_data_from_excel
from data_manager import sort_workers
from atoms import ColorChangingButton2
from widgets import SideMenu
from datetime import datetime, date
import pandas as pd
import tkinter as tk



def create_app():
    root = tk.Tk()
    root.title("Custom Button Test")
    SideMenu(root)



    root.mainloop()

# Run the application
create_app()