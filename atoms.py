import tkinter as tk

class ColorChangingButton:
    def __init__(self, master, text, command=None, grid_options=None):
        self.master = master
        self.command = command
        self.active = False

        # Create frame and label
        self.frame = tk.Frame(master, bg="white", bd=1)
        self.label = tk.Label(self.frame, text=text, bg="white", fg="black")

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
        self.frame.config(bg="light blue")
        self.label.config(bg="light blue", fg="black")

def deactivate_other_buttons(except_button):
    for button in buttons:
        if button != except_button:
            button.deactivate_button()



class TourItem(tk.Frame):
    """
    A custom Tkinter Frame widget representing a tour item.

    Parameters:
    - master: The parent widget.
    - number (str): The number of the tour.
    - time (str): Time associated with the tour, used to set initial toggle state.
    - delete_callback (function): A callback function to handle deletion of the tour item.

    Attributes:
    - label: Displays the tour number.
    - button1, button2, button_other: Toggle buttons for selecting tour types.
    - edit_field: An entry field for input, visible when 'other' is selected.
    - delete_button: A red, round button to delete this tour item.
    - toggle_state: The current state of the toggle buttons.
    - stored_time: The saved time value for the tour item.
    """
    def __init__(self, master, number, time, delete_callback):
        super().__init__(master)
        self.number = number
        self.stored_time = time
        self.delete_callback = delete_callback
        self.toggle_state = None

        self.label = tk.Label(self, text=f"{number}", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=16)

        self.button1 = ColorChangingButton(self, text="1", command=lambda: self.set_toggle_state("1"), grid_options={'row': 0, 'column': 1})
        self.button2 = ColorChangingButton(self, text="2", command=lambda: self.set_toggle_state("2"), grid_options={'row': 0, 'column': 2})
        self.button_other = ColorChangingButton(self, text="?", command=lambda: self.set_toggle_state("other"), grid_options={'row': 0, 'column': 3})

        self.edit_field = tk.Entry(self, width=6)
        self.whitespace = tk.Label(self, width=6)  # Placeholder for whitespace
        self.whitespace.grid(row=0, column=4, padx=8)

        delete_button = tk.Button(self, text="x", command=self.delete, bg="red", fg="white", font=("Arial", 12), height=2, width=2)
        delete_button.config(borderwidth=0, highlightthickness=0)
        delete_button.grid(row=0, column=5, padx=8, pady=8)

        self.set_initial_state(time)

    def set_toggle_state(self, state):
        self.toggle_state = state
        for button in [self.button1, self.button2, self.button_other]:
            button.deactivate_button()

        if state == "1":
            self.button1.activate_button()
            self.edit_field.grid_remove()
            self.whitespace.grid()
        elif state == "2":
            self.button2.activate_button()
            self.edit_field.grid_remove()
            self.whitespace.grid()
        elif state == "other":
            self.button_other.activate_button()
            self.whitespace.grid_remove()
            self.edit_field.grid(row=0, column=4,padx=7)

    def set_initial_state(self, time):
        if time in ["1", "2"]:
            self.set_toggle_state(time)
        else:
            self.set_toggle_state("other")
            self.edit_field.insert(0, time)

    def get_time(self):
        return self.stored_time if self.toggle_state == "other" else self.toggle_state

    def delete(self):
        self.delete_callback(self.number)
        self.destroy()


class TourItemCreator(tk.Frame):
    """
    A widget for creating new TourItem instances.
    """
    def __init__(self, parent, add_callback):
        super().__init__(parent)
        self.add_callback = add_callback

        # Entry for setting the Tour number
        self.number_entry = tk.Entry(self)
        self.number_entry.pack(side="left", padx=5)

        # Add button to create a new TourItem
        self.add_button = tk.Button(self, text="Add", command=self.add_tour)
        self.add_button.pack(side="left", padx=5)

        # Delete button to remove this creator widget
        self.delete_button = tk.Button(self, text="Delete", command=self.destroy)
        self.delete_button.pack(side="left", padx=5)

    def add_tour(self):
        # Retrieve number from entry and call the add_callback function
        number = self.number_entry.get()
        if number:
            self.add_callback(number)
            self.number_entry.delete(0, tk.END)  # Clear the entry after adding
