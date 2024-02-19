import tkinter as tk
import ttkbootstrap as ttk
from atoms import TourItem2

root = ttk.Window(themename="superhero")
root.title("Tagesplanung")
root.geometry("440x400")
touritem = TourItem2(root, 11, 0)
touritem.frame.pack()

root.mainloop()




