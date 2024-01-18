import tkinter as tk

class ColorChangingButton:
    def __init__(self, master, text, command=None, grid_options=None):
        self.master = master
        self.command = command
        self.active = False

        # Create frame and label
        self.frame = tk.Frame(master, bg="light grey", bd=1)
        self.label = tk.Label(self.frame, text=text, bg="light grey", fg="black")

        self.label.pack(expand=True, fill="both")
        
        # Use grid manager if grid options are provided, else default to pack
        if grid_options:
            self.frame.grid(**grid_options)
        else:
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





class TourItem(tk.Frame):
    """
    should take 1/2 as argument to be constrcucted instead of time, only use time if "other" is clicked
    on construction. 
    Should be usable as a creation element as well.
    Default one toggle button needs to be colored. 
    Stock white space the same size as the edit field that might pop up
    Fix Name 
    Check if it still works with the Menu that has been using it prebiously
    
    
    """
    
    def __init__(self, master, number, time, delete_callback):
        super().__init__(master)
        self.number = number
        self.time = time
        self.delete_callback = delete_callback
        self.toggle_state = None

        # Display Tour number and time
        self.label = tk.Label(self, text=f"Tour {number:03d} - {time}", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, sticky="w")

        # ColorChangingButtons for "1", "2", and "other"
        self.button1 = ColorChangingButton(self, text="1", command=lambda: self.set_toggle_state("1"), grid_options={'row': 0, 'column': 1})
        self.button2 = ColorChangingButton(self, text="2", command=lambda: self.set_toggle_state("2"), grid_options={'row': 0, 'column': 2})
        self.button_other = ColorChangingButton(self, text="other", command=lambda: self.set_toggle_state("other"), grid_options={'row': 0, 'column': 3})


        # Edit field, initially hidden
        self.edit_field = tk.Entry(self)
        self.edit_field.grid(row=0, column=4)
        self.edit_field.grid_remove()  # Hide initially

        # Delete button
        delete_button = tk.Button(self, text="Delete", command=self.delete)
        delete_button.grid(row=0, column=5)

    def set_toggle_state(self, state):
        # Update the toggle state and button appearances
        self.toggle_state = state
        for button in [self.button1, self.button2, self.button_other]:
            button.deactivate_button()

        if state == "1":
            self.button1.activate_button()
            self.edit_field.grid_remove()
        elif state == "2":
            self.button2.activate_button()
            self.edit_field.grid_remove()
        elif state == "other":
            self.button_other.activate_button()
            self.edit_field.grid()

    def delete(self):
        # Communicate back to TageKonfigurieren that this item is deleted
        self.delete_callback(self.number)
        self.destroy()