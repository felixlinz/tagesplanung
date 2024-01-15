import tkinter as tk

class ColorChangingButton:
    def __init__(self, master, text, command=None):
        self.master = master
        self.command = command
        self.active = False

        # Create frame and label
        self.frame = tk.Frame(master, bg="light grey", bd=1)
        self.label = tk.Label(self.frame, text=text, bg="light grey", fg="black")

        self.label.pack(expand=True, fill="both")
        self.frame.pack(fill="x")

        # Bind events
        self.frame.bind("<Enter>", self.on_enter)
        self.frame.bind("<Leave>", self.on_leave)
        self.frame.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        if not self.active:
            self.frame.config(bg="light blue")
            self.label.config(bg="light blue")

    def on_leave(self, event):
        if not self.active:
            self.frame.config(bg="light grey")
            self.label.config(bg="light grey")

    def on_click(self, event):
        self.activate_button()
        if self.command:
            self.command(self)

    def activate_button(self):
        self.active = True
        self.frame.config(bg="dark blue")
        self.label.config(bg="dark blue", fg="white")

    def deactivate_button(self):
        self.active = False
        self.frame.config(bg="light grey")
        self.label.config(bg="light grey", fg="black")

def menu_command(clicked_button):
    # Reset all buttons except the clicked one
    for button in buttons:
        if button != clicked_button:
            button.deactivate_button()

# Create main window
root = tk.Tk()
root.title("Side Menu Example")

# Create a list to store buttons
buttons = []

# Create and add buttons to the list
for i in range(5):
    button = ColorChangingButton(root, f"Menu Item {i+1}", menu_command)
    buttons.append(button)

root.mainloop()
