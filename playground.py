import tkinter as tk
import ttkbootstrap as ttk


def rewrite():
    string_var.set("AMK")
    

root = ttk.Window()
root.geometry("400x400")
root.title("playground")

stringvar = tk.StringVar(value="StringVarValue")
boolvar = tk.BooleanVar(value=False)

def bfunc():
    print("a basic button")

button = ttk.Button(root, command=bfunc, textvariable=stringvar)
button.pack()

check = ttk.Checkbutton(root, text="checkbox", variable=boolvar, command= lambda: print(boolvar.get()))
check.pack()


root.mainloop()