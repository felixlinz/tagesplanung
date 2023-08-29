import pandas as pd
import tkinter as tk
from tkinter import ttk

class TourSelectionGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tour Selection")
        
        # Widgets list for reference
        self.widgets = []
        
        # Data for saving selections
        self.df_data = []
        
        # Initial page
        self.show_main_page(self)


    def toggle_wave(self, btn):
        current_text = btn["text"]
        btn["text"] = "2. Welle" if current_text == "1. Welle" else "1. Welle"

    def save_and_exit(self):
        self.df_data = []
        tour_data = []
        for i, (chk_var, switch_btn) in enumerate(self.widgets):
            if chk_var.get():
                tour_number = f"{i+1:03}"
                wave = switch_btn["text"]
                tour_data.append([tour_number, wave])
        
        self.df_data = pd.DataFrame(tour_data, columns=['Tour', 'Welle'])
        self.root.destroy()

    @classmethod
    def show_main_page(cls, instance):
        if not instance:
            instance = cls()

        # Clear previous widgets
        for widget in instance.root.winfo_children():
            widget.destroy()

        # Entry box for "Number of tours"
        ttk.Label(instance.root, text="Number of tours:").pack(padx=5, pady=5)
        num_tours_var = tk.StringVar()
        num_tours_entry = ttk.Entry(instance.root, textvariable=num_tours_var)
        num_tours_entry.pack(padx=5, pady=5)

        weiter_button = ttk.Button(instance.root, text="Weiter", command=instance.save_and_exit)
        weiter_button.pack(padx=5, pady=5, anchor=tk.NE)
        
        zurück_button = ttk.Button(instance.root, text="Zurück", command=instance.show_previous_page)  # Stubbed method
        zurück_button.pack(padx=5, pady=5, anchor=tk.SW)

        # Main frame
        main_frame = ttk.Frame(instance.root)
        main_frame.pack(padx=5, pady=5)

        # Create two frames for the columns of tours
        left_frame = ttk.Frame(main_frame)
        right_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)
        right_frame.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)

        def update_tours(*args):
            instance.widgets = []
            for frame in [left_frame, right_frame]:
                for widget in frame.winfo_children():
                    widget.destroy()

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
                    switch_btn = ttk.Button(frame, text="1. Welle", command=lambda btn=switch_btn: instance.toggle_wave(btn))
                    switch_btn.grid(row=i // 2, column=2, padx=5, pady=5)
                    
                    # Store the widget references
                    instance.widgets.append((cb_var, switch_btn))

            except ValueError:
                pass

        num_tours_var.trace_add("write", update_tours)
        instance.root.mainloop()

    def show_previous_page(self):
        # Stub method for now
        pass


import tkinter as tk
from tkinter import ttk
import pandas as pd

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

