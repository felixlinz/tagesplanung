import pandas as pd
import tkinter as tk
from tkinter import ttk
import pandas as pd

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
        self.pages = [self.page_one, self.page_two]
        self.current_page_index = 0

        # Display initial page
        self.pages[self.current_page_index]()
        
        # Variables for Tour and Beiwagen Count
        self.selected_tour_amount = None
        self.selected_beiwagen_amount = None
        
        # list for the data figuered out in clickable list
        
    def get_selected_tours(self):
        selected_tours = set()

        for idx, (chk_var, radio_var) in enumerate(self.tour_selections, 1):
            if chk_var.get():
                tour = f"{idx:03}" 
                wave = "1" if radio_var.get() == "1. Welle" else "2"
                selected_tours.add((tour, wave))

        return selected_tours



    def clear_frame(self):
        for widget in self.page_frame.winfo_children():
            widget.destroy()

    def page_one(self):
        self.clear_frame()

        # Label for "Number of tours:"
        lbl_tours = ttk.Label(self.page_frame, text="Touren:")
        lbl_tours.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W)

        # Spinbox for tour selection
        self.tour_amount = tk.StringVar(value="29")  # default value set to 29
        spinbox_tours = ttk.Spinbox(self.page_frame, from_=1, to=100, textvariable=self.tour_amount, increment=1, width=5)
        spinbox_tours.grid(row=0, column=1, padx=20, pady=20, sticky=tk.W)

        # Label for "Beiwagen"
        lbl_beiwagen = ttk.Label(self.page_frame, text="Beiwagen:")
        lbl_beiwagen.grid(row=1, column=0, padx=20, pady=20, sticky=tk.W)

        # Spinbox for "Beiwagen"
        self.beiwagen_amount = tk.StringVar(value="2")  # default value set to 2
        spinbox_beiwagen = ttk.Spinbox(self.page_frame, from_=1, to=100, textvariable=self.beiwagen_amount, increment=1, width=5)
        spinbox_beiwagen.grid(row=1, column=1, padx=20, pady=20, sticky=tk.W)


    def page_two(self):
        self.clear_frame()

        # Generate tour list with checkbox and radio buttons
        self.tour_selections = []

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
            
        # Increment page and show
        self.current_page_index += 1
        if self.current_page_index < len(self.pages):
            self.pages[self.current_page_index]()
        


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = TourGui()
    gui.run()


def create_gui():
    root = tk.Tk()
    root.title("Tour Selection")
    
    # To store the final DataFrame
    df_data = []

    # Function to toggle between 1.Welle and 2.Welle
    def toggle_wave(btn):
        current_text = btn["text"]
        btn["text"] = "2. Welle" if current_text == "1. Welle" else "1. Welle"

    # Function to save the selected data
    def save_and_exit():
        nonlocal df_data
        tour_data = []
        for i, (chk_var, switch_btn) in enumerate(widgets):
            if chk_var.get():
                tour_number = f"{i+1:03}"
                wave = switch_btn["text"]
                tour_data.append([tour_number, wave])
        
        df_data = pd.DataFrame(tour_data, columns=['Tour', 'Welle'])
        root.destroy()

    # Entry box for "Number of tours"
    ttk.Label(root, text="Number of tours:").pack(padx=5, pady=5)
    num_tours_var = tk.StringVar()
    num_tours_entry = ttk.Entry(root, textvariable=num_tours_var)
    num_tours_entry.pack(padx=5, pady=5)

    weiter_button = ttk.Button(root, text="Weiter", command=save_and_exit)
    weiter_button.pack(padx=5, pady=5, anchor=tk.NE)

    # Main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=5, pady=5)

    # Create two frames for the columns of tours
    left_frame = ttk.Frame(main_frame)
    right_frame = ttk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)
    right_frame.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)

    # A list to store widget references
    widgets = []

    def update_tours(*args):
        for frame in [left_frame, right_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        del widgets[:]

        try:
            n = int(num_tours_var.get())
            for i in range(n):
                frame = left_frame if i % 2 == 0 else right_frame

                # Checkbox
                cb_var = tk.BooleanVar(value=True)
                chk = ttk.Checkbutton(frame, variable=cb_var)
                chk.grid(row=i // 2, column=0, padx=5, pady=5)

                # Tour number label
                lbl = ttk.Label(frame, text=f"{i+1:03}")
                lbl.grid(row=i // 2, column=1, padx=5, pady=5)

                # Toggle button
                switch_btn = ttk.Button(frame, text="1. Welle", command=lambda btn=switch_btn: toggle_wave(btn))
                switch_btn.grid(row=i // 2, column=2, padx=5, pady=5)
                
                # Store the widget references
                widgets.append((cb_var, switch_btn))

        except ValueError:
            pass

    num_tours_var.trace_add("write", update_tours)
    root.mainloop()

    return df_data

