from atoms import TourItem

from tkinter import scrolledtext
import tkinter as tk

# Assuming TourItem class is already defined

def create_tour_items():
    root = tk.Tk()
    root.title("Tour Items List")

    frame = scrolledtext.ScrolledText(root)
    frame.pack(fill=tk.BOTH, expand=True)

    for i in range(1, 21):
        number = f"{i:03d}"
        time = "1"  # Default time, can be changed as needed
        tour_item = TourItem(frame, number, time, delete_callback=lambda num: print(f"Deleted Tour {num}"))
        tour_item.pack(pady=2, padx=2, fill=tk.X)

    root.mainloop()

create_tour_items()