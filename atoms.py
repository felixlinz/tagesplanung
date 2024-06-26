import tkinter as tk
import ttkbootstrap as ttk


class ColorChangingButton:
    def __init__(self, master, text, active_color="gray72", inactive_color="gray85", command=None, grid_options=None, effort=None):
        self.master = master
        self.command = command
        self.active = False
        self.effort = effort
        self.active_color = active_color
        self.inactive_color = inactive_color

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
        self.bind_widgets("<Button-1>", self.on_click)

    def bind_widgets(self, event, handler):
        self.frame.bind(event, handler)
        self.label.bind(event, handler)


    def on_click(self, event):
        self.activate_button()
        if self.command:
            self.command()

    def activate_button(self):
        self.active = True
        self.frame.config(bg=self.active_color)
        self.label.config(bg=self.active_color, fg="black")

    def deactivate_button(self):
        self.active = False
        self.frame.config(bg=self.inactive_color)
        self.label.config(bg=self.inactive_color, fg="black")
        
        
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
        self.command=command

        # Create frame with a specified width (96 px) and height (adjusting for top and bottom padding)
        self.frame = tk.Frame(self.master.frame, bg=self.inactive_color, bd=1, width=196, height=36)  # Height is an estimate; adjust as needed
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

class OptionalEntry:
    def __init__(self, master, entry_value):
        self.active = False
        self.entry_var = tk.StringVar(value = entry_value)
        self.frame = ttk.Frame(master, height="32", width="54")
        self.entry = ttk.Entry(self.frame, textvariable=self.entry_var)
        self.frame.pack_propagate(False)
        
    def activate(self):
        self.active = True
        self.entry.pack(fill = "both", expand=True)  
        
    
    def deactivate(self):
        self.active = False
        self.entry.pack_forget()
        
    def get(self):
        return self.entry.get()



class ColorChangingButton3:
    def __init__(self, master, label, index, active_color="gray84", inactive_color="white", command=None, grandparent=None):
        self.grandparent = grandparent
        self.index = index
        self.frame = tk.Frame(master, width=32, height=32)
        self.active = False
        self.label = tk.Label(self.frame, text = label, font="Myriad")
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.other_buttons = []
        self.command = command
        
        self.bind_widgets("<Button-1>", self.on_click)
        
        self.label.place(relx="0.5", rely="0.5", anchor="center")
        
        self.frame.pack_propagate(False)

        
    def add_other_buttons(self, neighbours):
        for neighbor in neighbours:
            if neighbor != self:
                self.other_buttons.append(neighbor)

    def bind_widgets(self, event, handler):
        self.frame.bind(event, handler)
        self.label.bind(event, handler)
        
    def on_click(self, event):
        self.activate_button()

    def activate_button(self):
        self.active = True
        self.deactivate_other_buttons()
        self.frame.config(bg=self.active_color)
        self.label.config(bg=self.active_color, fg="black")
        if self.command:
            self.command(True)
        if self.grandparent:
            self.grandparent.activate_save_buttons()
        
        
    def deactivate_button(self):
        self.active = False
        self.frame.config(bg=self.inactive_color)
        self.label.config(bg=self.inactive_color, fg="gray54")    
        if self.command:
            self.command(False)
        
    def add_other_buttons(self, buttons):
        self.other_buttons = [button for button in buttons if button != self]
        
    def deactivate_other_buttons(self):
        if self.other_buttons:
            for button in self.other_buttons:
                button.deactivate_button()

        
class TimeCaptureUnit:
    def __init__(self, master, delete_function):
        self.master = master
        self.delete_function = delete_function
        self.frame = ttk.Frame(self.master)
        self.jobvariable = tk.StringVar()
        self.timevariable = tk.StringVar()
        self.job_entry = ttk.Entry(self.frame, textvariable=self.jobvariable )
        self.time_entry = ttk.Entry(self.frame, textvariable=self.timevariable, width="4")
        self.delete_button = ttk.Button(self.frame, text="-", command=self.delete)
        self.job_entry.pack(side= "left")
        self.time_entry.pack(side="left", padx="8")
        self.delete_button.pack(side="left")
        
    def delete(self):
        self.delete_function(self)
      
    def values(self):
        data = (self.jobvariable.get(), self.timevariable.get())
        return data
    
    
class TimeFilledUnit:
    def __init__(self, master, job, time, delete_function):
        self.master = master
        self.delete_function = delete_function
        self.frame = ttk.Frame(self.master)
        self.jobvariable = tk.StringVar(value= job)
        self.timevariable = tk.StringVar(value= time)
        self.delete_button = ttk.Button(self.frame, text="-", command=self.delete)
        self.job_entry = ttk.Entry(self.frame, textvariable=self.jobvariable )
        self.time_entry = ttk.Entry(self.frame, textvariable=self.timevariable, width="4")
        self.job_entry.pack(side= "left")
        self.time_entry.pack(side="left", padx="8")
        self.delete_button.pack(side="left")
    
    def delete(self):
        self.delete_function(self)
    
    def values(self):
        return (self.jobvariable.get(), self.timevariable.get())
            
            
            
class ToggleButton(tk.Frame):
    def __init__(self, master, labels, command=None):
        super().__init__(master)
        self.labels = labels
        self.command = command
        self.buttons = []
        self.configure(bg='white') 
        self.state = 0

        for idx, label in enumerate(self.labels):
            button = ColorChangingButton(self, label=label, command=lambda idx=idx: self.set_active_button(idx), grid_options={'row': 0, 'column': idx})
            self.buttons.append(button)
            

        # Set the first button as active by default
        self.set_active_button(self.state)

    def set_active_button(self, active_index):
        # Update the active button and deactivate others
        self.buttons[active_index].activate_button()
        
    def return_state(self):
        for n ,button in enumerate(self.buttons):
            if button.active == True:
                return n
                
                
                
class ToggleButton2:
    def __init__(self, master, labels, state=0, active_color="gray72", inactive_color="gray85", command=None, command_button_index = -1):
        self.frame = ttk.Frame(master)
        
        self.active_color = active_color
        self.inctive_color = inactive_color
        self.labels = labels
        self.command = command
        self.buttons = []   
        self.state = state
        self.command_index = command_button_index
        
        for n, label in enumerate(self.labels):
            self.buttons.append(ColorChangingButton3(self.frame, label, index= n, active_color=self.active_color))
        
        
        for button in self.buttons:
            button.add_other_buttons(self.buttons)
            button.frame.pack(side= "left")
            
        self.buttons[self.state].activate_button()
        
        if self.command:
            self.buttons[self.command_index].command = self.command
        
        
    def set_active_button(self, active_index):
        # Update the active button and deactivate others
        self.buttons[active_index].activate_button()   
        
    def return_state(self):
        for n ,button in enumerate(self.buttons):
            if button.active == True:
                return n
        
    
            
            

class TourItem(tk.Frame):
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
        self.toggle_button = ToggleButton(self, labels=["1.","2.","3."], command=self.set_toggle_state)
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
        # self.delete_callback(self.number)
        self.destroy()


class TourItem2:
    def __init__(self, master, number, wave, delete = None):
        self.frame = ttk.Frame(master)
        self.number = number
        self.wave = int(wave-1)
        self.entry_frame = ttk.Frame(self.frame, width=128, height=32)
        self.entry = ttk.Entry(self.entry_frame)
        self.entry_frame.pack()
        self.toggle = ToggleButton2(self.frame, ["1", "2", "3"], state = wave, command=self.entry_state)
        self.toggle.frame.pack()
        
        self.delete = delete        

    def entry_state(self, state):
        if state == True:
            self.entry.pack()
        else:
            self.entry.pack_forget()
            




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


