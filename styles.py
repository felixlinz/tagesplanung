from tkinter import ttk

def set_styles():
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TButton', padding=12)
    style.configure('Accent.TButton', foreground='white', background='#0078D7')
