import tkinter as tk

def on_menu_click(item):
    print(f"{item} clicked")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Side Menu Example")

# Set the size of the window (you can adjust this as needed)
root.geometry('400x300')

# Create a frame for the side menu
side_menu = tk.Frame(root, bg="#eeeeee", padx=10, pady=10)
side_menu.pack(side=tk.LEFT, fill=tk.Y, expand=True)

# Define colors for the buttons
button_bg = "#ffffff"  # white background
button_fg = "#000000"  # black text

# Add menu items to the side menu frame
tagesplanung_btn = tk.Button(side_menu, text="Tagesplanung", bg=button_bg, fg=button_fg, command=lambda: on_menu_click("Tagesplanung"))
tagesplanung_btn.pack(fill=tk.X, padx=5, pady=5)

zeiten_btn = tk.Button(side_menu, text="Zeiten", bg=button_bg, fg=button_fg, command=lambda: on_menu_click("Zeiten"))
zeiten_btn.pack(fill=tk.X, padx=5, pady=5)

tage_btn = tk.Button(side_menu, text="Tage", bg=button_bg, fg=button_fg, command=lambda: on_menu_click("Tage"))
tage_btn.pack(fill=tk.X, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
