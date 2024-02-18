import tkinter as tk
import ttkbootstrap as ttk


root = ttk.Window(themename="superhero")
root.title("Tagesplanung")
root.geometry("440x1200")



subframe = ttk.Frame(root)
entry = ttk.Entry(subframe)
label = ttk.Label(subframe, text="label", font="Arial 64 bold")
button = ttk.Button(subframe, text="Klick mich", )
entry.pack()
label.pack(padx=64, pady=64)
subframe.pack(pady = 64)

textfield = ttk.Text(root)
textfield.pack(padx=64, pady=64)

root.mainloop()
