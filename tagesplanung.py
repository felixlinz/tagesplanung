import tkinter as tk
import ttkbootstrap as ttk

root = ttk.Window(themename="superhero")
root.title("Tagesplanung")
root.geometry("440x400")



subframe = ttk.Frame(root)
entry = ttk.Entry(subframe)
label = ttk.Label(subframe, text="label", font="Arial 64 bold")
entry.pack()
label.pack(padx=64, pady=64)
subframe.pack()

textfield = ttk.Text(root)
textfield.pack(padx=64, pady=64)

root.mainloop()

