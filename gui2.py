import tkinter as tk
from tkinter import ttk


# Main application class
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('tagesplanung')
        self.geometry('962x720')

        # Set styles for buttons
        self.set_styles()

        # Create the sidebar
        self.sidebar = Sidebar(self, width=212)
        self.sidebar.pack(side='left', fill='y')

        # Create the main content area
        self.main_content = tk.Frame(self)
        self.main_content.pack(side='right', fill='both', expand=True)

        # Initialize pages
        self.pages = {}
        self.current_page = None
        self.index = 0  # Index for page navigation

        # Create a frame for the navigation buttons at the bottom of the main content area
        self.nav_frame = tk.Frame(self.main_content)
        self.nav_frame.pack(side='bottom', fill='x')

        # Add navigation buttons
        self.back_button = ttk.Button(self.nav_frame, text='Zurück', command=self.prev_page)
        self.back_button.pack(side='left')

        self.forward_button = ttk.Button(self.nav_frame, text='Weiter', style='Accent.TButton', command=self.next_page)
        self.forward_button.pack(side='right')

        # ... (rest of the Application class methods)

    def set_styles(self):
        style = ttk.Style()
        style.theme_use('default')

        # Sidebar button style (macOS Finder-like)
        style.configure('Sidebar.TButton', background='lightgrey', foreground='black', borderwidth=0, padding=6, focuscolor='lightgrey')

        # Active sidebar button style
        style.configure('ActiveSidebar.TButton', background='lightblue', foreground='black', borderwidth=0, padding=6, focuscolor='blue')

        # Map background for hover effect to be consistent
        style.map('Sidebar.TButton', background=[('active', 'lightgrey'), ('!active', 'lightgrey')])
        style.map('ActiveSidebar.TButton', background=[('active', 'lightblue'), ('!active', 'lightblue')])

        
    def add_page(self, page_class, page_name):
        page = page_class(self.main_content)
        self.pages[page_name] = page

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[page_name]
        self.current_page.pack(fill='both', expand=True)

    def next_page(self):
        page_names = list(self.pages.keys())
        self.index = (self.index + 1) % len(page_names)
        self.show_page(page_names[self.index])

    def prev_page(self):
        page_names = list(self.pages.keys())
        self.index = (self.index - 1) % len(page_names)
        self.show_page(page_names[self.index])

class Sidebar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg='lightgrey', highlightbackground='darkgrey', highlightthickness=1)
        self.buttons = {}
        self.create_buttons()
        self.set_active('Tagesplanung')  # Set the initial active button

    def create_buttons(self):
        self.buttons['Tagesplanung'] = ttk.Button(self, text='Tagesplanung', style='Sidebar.TButton', command=lambda: self.set_active('Tagesplanung'), takefocus=False)
        self.buttons['Tagesplanung'].pack(fill='x')

        self.buttons['Wochentage konfigurieren'] = ttk.Button(self, text='Wochentage konfigurieren', style='Sidebar.TButton', command=lambda: self.set_active('Wochentage konfigurieren'), takefocus=False)
        self.buttons['Wochentage konfigurieren'].pack(fill='x')

        self.buttons['Settings'] = ttk.Button(self, text='Settings', style='Sidebar.TButton', command=lambda: self.set_active('Settings'), takefocus=False)
        self.buttons['Settings'].pack(fill='x')

    def set_active(self, active_button):
        for button in self.buttons.values():
            button['style'] = 'Sidebar.TButton'
        self.buttons[active_button]['style'] = 'ActiveSidebar.TButton'
        # You can also trigger a page change or other action here


# Page template class
class Page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text="This is a page")
        label.pack()

