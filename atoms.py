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

        # Enable the frame to take focus
        self.frame.focus_set()

        # Bind events to both frame and label
        self.bind_widgets("<Enter>", self.on_enter)
        self.bind_widgets("<Leave>", self.on_leave)
        self.bind_widgets("<Button-1>", self.on_click)

    def bind_widgets(self, event, handler):
        self.frame.bind(event, handler)
        self.label.bind(event, handler)

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
            self.command()

    def activate_button(self):
        self.active = True
        self.frame.config(bg="#007aff")
        self.label.config(bg="#007aff", fg="white")

    def deactivate_button(self):
        self.active = False
        self.frame.config(bg="light grey")
        self.label.config(bg="light grey", fg="black")

def deactivate_other_buttons(except_button):
    for button in buttons:
        if button != except_button:
            button.deactivate_button()



