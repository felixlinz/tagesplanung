import tkinter as tk


class ColorChangingButton:
    def __init__(self, master, text, command=None, grid_options=None, effort=None):
        self.master = master
        self.command = command
        self.active = False
        self.effort = effort

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
        
        
class ColorChangingButton2:
    def __init__(self, master, text, grid_options=None, active_color="gray72", inactive_color="gray85", command=None):
        self.master = master
        self.other_buttons = []
        self.active = False
        self.active_color = active_color
        self.font_color = "black"
        self.font = ("Myriad Pro","12")
        self.inactive_color = inactive_color
        self.text=text
        self.command=None

        # Create frame with a specified width (96 px) and height (adjusting for top and bottom padding)
        self.frame = tk.Frame(master, bg=self.inactive_color, bd=1, width=196, height=36)  # Height is an estimate; adjust as needed
        self.frame.pack_propagate(False)  # Prevent the frame from resizing to fit the label

        # Create label with left padding of 16px and align it left; add 4px padding to the top and bottom
        self.label = tk.Label(self.frame, font=self.font, text=text, bg=self.inactive_color, fg="black", anchor="w")
        self.label.pack(fill="both", expand=True, padx=(32, 0), pady=(8, 8))
        
        # Use grid manager if grid options are provided, else default to pack
        if grid_options:
            self.frame.grid(**grid_options)
        else:
            self.frame.pack(fill="x")

        # Enable the frame to take focus
        self.frame.focus_set()

        # Bind events to both frame and label
        self.bind_widgets("<Button-1>", self.on_click)
        
    def add_other_buttons(self, neighbours):
        for neighbor in neighbours:
            if neighbor != self:
                self.other_buttons.append(neighbor)

    def bind_widgets(self, event, handler):
        self.frame.bind(event, handler)
        self.label.bind(event, handler)


    def on_click(self, event):
        self.activate_button()
        if self.command:
            self.command()

    def activate_button(self):
        self.active = True
        self.deactivate_other_buttons()
        self.frame.config(bg=self.active_color)
        self.label.config(bg=self.active_color, fg=self.font_color)
        

    def deactivate_button(self):
        self.active = False
        self.frame.config(bg=self.inactive_color)
        self.label.config(bg=self.inactive_color, fg="black")
        
    def deactivate_other_buttons(self):
        for button in self.other_buttons:
            button.deactivate_button()


            
            
            
class ToggleButton(tk.Frame):
    """
    A custom Tkinter Frame widget that groups together a set of toggle buttons.

    Attributes:
    - callback (function): A callback function invoked when a toggle button is pressed.
    - buttons (list): A list of ColorChangingButton instances.
    - current_state (str): The label of the currently active button.

    Methods:
    - set_active_button: Activates a button at the given index and deactivates others.
    - get_active_button_label: Returns the label of the currently active button.
    """
    def __init__(self, master, callback=None):
        super().__init__(master)
        self.labels = ["1", "2", "?"]
        self.callback = callback
        self.buttons = []
        self.configure(bg='white') 

        for idx, label in enumerate(self.labels):
            button = ColorChangingButton(self, text=label, command=lambda idx=idx: self.set_active_button(idx), grid_options={'row': 0, 'column': idx})
            self.buttons.append(button)
            

        # Set the first button as active by default
        self.set_active_button(0)

    def set_active_button(self, active_index):
        # Update the active button and deactivate others
        for idx, button in enumerate(self.buttons):
            if idx == active_index:
                button.activate_button()
                if self.callback:
                    self.callback(button.label['text'])
            else:
                button.deactivate_button()
                
    
            
            

class TourItem(tk.Frame):
    """
    A custom Tkinter Frame widget representing a tour item.

    Attributes:
    - number (str): The number of the tour.
    - stored_time (str): Time associated with the tour, used to set the initial toggle state.
    - delete_callback (function): A callback function to handle the deletion of the tour item.
    - toggle_state (str): The current state of the toggle buttons.
    - label (tk.Label): A label displaying the tour number.
    - edit_field (tk.Entry): An entry field for input, visible when 'other' is selected.
    - whitespace (tk.Label): A label acting as a placeholder for layout consistency.
    - toggle_button (ToggleButton): A set of toggle buttons for selecting tour types.
    - delete_button (tk.Button): A button to delete the tour item.

    Methods:
    - set_toggle_state: Sets the state of the toggle buttons and updates the UI accordingly.
    - set_initial_state: Sets the initial state of the toggle buttons based on provided time.
    - get_time: Returns the stored time or the current state of the toggle buttons.
    - delete: Deletes the tour item and performs callback.
    """
    def __init__(self, master, number, time, delete_callback):
        super().__init__(master, bg="white")
        self.number = number
        self.stored_time = time
        self.delete_callback = delete_callback
        self.toggle_state = None

        # Layout configuration
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)  # Adjust weight for toggle button

        # Tour number label
        self.label = tk.Label(self, text=f"{number}", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=16)

        # Edit field and whitespace
        self.edit_field = tk.Entry(self, width=6)
        self.whitespace = tk.Label(self, width=1, bg="white")
        self.whitespace.grid(row=0, column=2, padx=8)
        
        # ToggleButton
        self.toggle_button = ToggleButton(self, callback=self.set_toggle_state)
        self.toggle_button.grid(row=0, column=1, columnspan=3, sticky="ew")

        # Delete button
        delete_button = tk.Button(self, text="x", command=self.delete, bg="red", fg="white", font=("Arial", 12), height=2, width=2)
        delete_button.config(borderwidth=0, highlightthickness=0)
        delete_button.grid(row=0, column=3, padx=8, pady=8)

        # Set initial toggle state
        self.set_initial_state(time)

    def set_initial_state(self, time):
        # Set the initial toggle state based on the time
        if time in ["1", "2"]:
            self.toggle_button.set_active_button(int(time) - 1)  # 0 for "1", 1 for "2"
        else:
            self.toggle_button.set_active_button(2)  # "other" button
            self.edit_field.insert(0, time)
            self.edit_field.grid(row=0, column=2, padx=7)
            
            
    def set_toggle_state(self, state):
        self.toggle_state = state
        # Handle toggle state changes here
        # For example, show/hide the edit field based on the state
        if state == "?":
            self.edit_field.grid(row=0, column=4, padx=7)
        else:
            self.edit_field.grid_remove()

    def get_time(self):
        # Return the stored time if "other" is selected, else return the button label
        active_label = self.toggle_button.get_active_button_label()
        return self.stored_time if active_label == "?" else active_label

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


