from data_manager import get_next_working_day
from data_manager import format_date_with_weekday
from data_manager import learn_data_from_excel
from data_manager import sort_workers
from atoms import ColorChangingButton2
from datetime import datetime, date
import pandas as pd
import tkinter as tk



def create_app():
    root = tk.Tk()
    root.title("Custom Button Test")


    names = ["Tag", "Zusteller", "Wochen"]
    # Placeholder for buttons list
    buttons = []

    # Create several ColorChangingButton2 instances
    for name in names:
        buttons.append(ColorChangingButton2(root, name))

    # Link buttons for mutual deactivation
    for button in buttons:
        button.add_other_buttons(buttons)

    root.mainloop()

# Run the application
create_app()