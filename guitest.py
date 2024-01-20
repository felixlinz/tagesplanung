from atoms import TourItem
from widgets import TageKonfigurieren
from tkinter import scrolledtext
import tkinter as tk

root = tk.Tk()
root.title("Tage Konfigurieren")

app = TageKonfigurieren(root)

root.mainloop()