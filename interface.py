import pandas as pd
import tkinter as tk
from tkinter import ttk
import data_manager
from datetime import date, timedelta, datetime
from workalendar.europe import Germany

class TourGui:
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("Tour Selection")

        # Define a frame to contain pages' content
        self.page_frame = ttk.Frame(self.root)
        self.page_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Navigation buttons
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.zuruck_btn = ttk.Button(self.nav_frame, text="Zurück", command=self.previous_page)
        self.zuruck_btn.pack(side=tk.LEFT)
        
        self.weiter_btn = ttk.Button(self.nav_frame, text="Weiter", command=self.next_page)
        self.weiter_btn.pack(side=tk.RIGHT)

        # Define pages in order
        self.pages = [self.page_one, self.page_two, self.page_three]
        self.current_page_index = 0


         #figuere out dates that are editable
        self.tomorrow = self.get_next_working_day(date.today())
        self.day_after = self.get_next_working_day(self.tomorrow)
        self.dates = [self.tomorrow, self.day_after, self.get_next_working_day(self.day_after)]
        self.selected_date = self.tomorrow
        
        
        # Display initial page
        self.pages[self.current_page_index]()
        
        # Variables for Tour and Beiwagen Count
        self.selected_tour_amount = None
        self.selected_beiwagen_amount = None
        
        self.tour_selections = []
        
        
    def get_selected_tours(self):
        selected_tours = set()

        for idx, (chk_var, radio_var) in enumerate(self.tour_selections, 1):
            
            tour = f"{idx:03}" 
            wave = "1" if radio_var.get() == "1. Welle" else "2"
            check = chk_var.get()
            selected_tours.add((tour, wave, check))

        return selected_tours



    def clear_frame(self):
        for widget in self.page_frame.winfo_children():
            widget.destroy()


    def page_one(self):
        self.clear_frame()


        # --- Date Selection ---
        date_frame = ttk.Frame(self.page_frame)
        date_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky=tk.W)

        # Single StringVar for all radio buttons
        self.selected_date = tk.StringVar()

        # Callback function to respond to date changes
        def on_date_change(*args):
            # Here, you can perform any other logic you might need when the date changes
            print(f"Selected date: {self.selected_date.get()}")

        self.selected_date.trace("w", on_date_change)

        for d in self.dates:
            date_str = d.strftime('%Y-%m-%d')
            ttk.Radiobutton(date_frame, text=date_str, variable=self.selected_date, value=date_str).pack(side=tk.LEFT, padx=10)

        # Default selection
        self.selected_date.set(self.dates[0])  # The first date is selected by default


        # --- Tour and Beiwagen Amount ---
        # Label for "Number of tours:"
        lbl_tours = ttk.Label(self.page_frame, text="Touren:")
        lbl_tours.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)

        # Spinbox for tour selection
        self.tour_amount = tk.StringVar(value="29")  # default value set to 29
        spinbox_tours = ttk.Spinbox(self.page_frame, from_=1, to=100, textvariable=self.tour_amount, increment=1, width=5)
        spinbox_tours.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W)

        # Label for "Beiwagen"
        lbl_beiwagen = ttk.Label(self.page_frame, text="Beiwagen:")
        lbl_beiwagen.grid(row=2, column=0, padx=20, pady=20, sticky=tk.W)

        # Spinbox for "Beiwagen"
        self.beiwagen_amount = tk.StringVar(value="2")  # default value set to 2
        spinbox_beiwagen = ttk.Spinbox(self.page_frame, from_=1, to=100, textvariable=self.beiwagen_amount, increment=1, width=5)
        spinbox_beiwagen.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W)


    def page_two(self):
        self.clear_frame()

        # Generate tour list with checkbox and radio button

        columns = 3
        rows_per_column = (self.selected_tour_amount + columns - 1) // columns

        # Create list of frames for columns
        column_frames = [ttk.Frame(self.page_frame) for _ in range(columns)]
        for i, frame in enumerate(column_frames):
            frame.grid(row=0, column=i*2, sticky='n')
            if i < columns - 1:
                separator = ttk.Separator(self.page_frame, orient='vertical')
                separator.grid(row=0, column=i*2+1, sticky='ns', pady=10)

        for i in range(self.selected_tour_amount):
            tour_number = f"{i + 1:03}"  # Format to "001", "002", etc.

            # Determine grid position
            row = i % rows_per_column
            col = i // rows_per_column

            # Checkbox
            chk_var = tk.BooleanVar(value=True)
            chkbox = ttk.Checkbutton(column_frames[col], text=tour_number, variable=chk_var)
            chkbox.grid(row=row, column=0, padx=20, sticky=tk.W)

            # Radio buttons for "1. Welle" and "2. Welle"
            radio_var = tk.StringVar(value="1. Welle")
            radio1 = ttk.Radiobutton(column_frames[col], text="1. Welle", variable=radio_var, value="1. Welle")
            radio1.grid(row=row, column=1, padx=(20, 0), pady=5)

            radio2 = ttk.Radiobutton(column_frames[col], text="2. Welle", variable=radio_var, value="2. Welle")
            radio2.grid(row=row, column=2, padx=(5, 20), pady=5)

            self.tour_selections.append((chk_var, radio_var))
            
    def page_three(self):
        self.clear_frame()
        # This page is empty for now
        lbl_placeholder = ttk.Label(self.page_frame, text="This is Page 3 (Placeholder).")
        lbl_placeholder.pack(pady=100)


    def previous_page(self):
        self.current_page_index = max(self.current_page_index - 1, 0)
        self.pages[self.current_page_index]()

    def next_page(self):
        # Save the selected values if on the first page
        if self.current_page_index == 0:
            self.selected_tour_amount = int(self.tour_amount.get())
            self.selected_beiwagen_amount = int(self.beiwagen_amount.get())
        # If on the second page, save the selected tours to a set
        elif self.current_page_index == 1:
            self.saved_selections = self.get_selected_tours()
            self.weiter_btn.config(text="Fertig")

        # Increment page and show
        self.current_page_index += 1
        
        if self.current_page_index < len(self.pages):
            self.pages[self.current_page_index]()
        
        if self.current_page_index == len(self.pages):
        # Assuming you are on the last page:
            self.root.destroy()  # This closes the main window
            
            
    def date_selected(self, selected_date):
        """
        Handler when a date is selected.
        """
        self.selected_date = selected_date
        # Any additional logic can be added here if you want UI updates based on date selection

    def get_next_working_day(self, current_day):
        cal = Germany()
        
        # Increment by one day to start
        next_day = current_day + timedelta(days=1)
        
        # While the next_day is a holiday or Sunday, keep moving to the next day
        while next_day.weekday() == 6 or cal.is_holiday(next_day): 
            next_day += timedelta(days=1)

        return next_day
        
        
    def save(self):
        """
        save
        """
        # Convert StringVar value to datetime.date object
        date_str = self.selected_date.get()
        selected_date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        data_manager.save_data(selected_date_obj, self.get_selected_tours())


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = TourGui()
    gui.run()



