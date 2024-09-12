import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import random
from collections import defaultdict


class COREapp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("COREwars Visualizer")
        self.geometry("900x650")

        # Initializing simulation settings
        self.wSize = 20
        self.sSpeed = 100
        self.gpturn = 50
        self.visibility_range = 1
        self.maxNumSoldiers = 1000
        self.startcount = 75
        self.step = 0
        self.displayStep = 0
        self.displaySuperStep = 0
        self.startingSuperStep = 0
        self.agent_set = set()
        self.agentLookup = {}
        self.faceLookup = {}
        self.superStep2Step = {}
        self.debug_mode = False
        self.timer = None
        self.aCount = random.randint(0, 3)

        # GUI elements initialization
        self.create_widgets()

    def create_widgets(self):
        # Create Tabbed Pane
        tabControl = ttk.Notebook(self)

        # Welcome Tab
        welcome_tab = ttk.Frame(tabControl)
        tabControl.add(welcome_tab, text='Welcome')

        # Add an image (as a label)
        try:
            img = Image.open("src/RAMfight.png")
            img = img.resize((450, 450), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(welcome_tab, image=img)
            panel.image = img
            panel.pack(side="top", fill="both", expand="yes")
        except Exception as e:
            panel = tk.Label(welcome_tab, text="Image Not Found", font=("Arial", 24))
            panel.pack()

        # Settings Tab
        settings_tab = ttk.Frame(tabControl)
        tabControl.add(settings_tab, text='Settings')

        # Settings Form
        form_frame = ttk.Frame(settings_tab, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        self.worldSize_var = tk.StringVar(value=f"World Size: {self.wSize}")
        world_size_label = ttk.Label(form_frame, textvariable=self.worldSize_var)
        world_size_label.grid(row=0, column=0, padx=5, pady=5)

        self.perTurn_var = tk.StringVar(value=f"New Fernies per Turn: {self.gpturn}")
        per_turn_label = ttk.Label(form_frame, textvariable=self.perTurn_var)
        per_turn_label.grid(row=1, column=0, padx=5, pady=5)

        self.visRange_var = tk.StringVar(value=f"Visibility Range: {self.visibility_range}")
        vis_range_label = ttk.Label(form_frame, textvariable=self.visRange_var)
        vis_range_label.grid(row=2, column=0, padx=5, pady=5)

        self.maxSoldiers_var = tk.StringVar(value=f"Max Fernies per Node: {self.maxNumSoldiers}")
        max_soldiers_label = ttk.Label(form_frame, textvariable=self.maxSoldiers_var)
        max_soldiers_label.grid(row=3, column=0, padx=5, pady=5)

        self.startCLabel_var = tk.StringVar(value=f"Starting Fernies: {self.startcount}")
        start_ferns_label = ttk.Label(form_frame, textvariable=self.startCLabel_var)
        start_ferns_label.grid(row=4, column=0, padx=5, pady=5)

        # Controls for Settings
        control_frame = ttk.Frame(settings_tab)
        control_frame.pack(fill=tk.BOTH, expand=True)

        set_ring_size_button = ttk.Button(control_frame, text="Set Ring Size", command=self.set_ring_size)
        set_ring_size_button.grid(row=0, column=0, padx=5, pady=5)

        set_growth_button = ttk.Button(control_frame, text="Set Fernies per Turn", command=self.set_growth)
        set_growth_button.grid(row=1, column=0, padx=5, pady=5)

        set_start_ferns_button = ttk.Button(control_frame, text="Set Starting Fernies", command=self.set_start_ferns)
        set_start_ferns_button.grid(row=2, column=0, padx=5, pady=5)

        set_max_button = ttk.Button(control_frame, text="Set Max per Tile", command=self.set_max_soldiers)
        set_max_button.grid(row=3, column=0, padx=5, pady=5)

        set_visibility_button = ttk.Button(control_frame, text="Set Visibility Range", command=self.set_visibility)
        set_visibility_button.grid(row=4, column=0, padx=5, pady=5)

        # Display Tab
        display_tab = ttk.Frame(tabControl)
        tabControl.add(display_tab, text='Display')

        # Simulation control buttons
        button_frame = ttk.Frame(display_tab)
        button_frame.pack(fill=tk.BOTH, expand=True)

        back_button = ttk.Button(button_frame, text="Back", command=self.step_backward)
        back_button.grid(row=0, column=0, padx=5, pady=5)

        play_button = ttk.Button(button_frame, text="Start", command=self.start_simulation)
        play_button.grid(row=0, column=1, padx=5, pady=5)

        pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_simulation)
        pause_button.grid(row=0, column=2, padx=5, pady=5)

        forward_button = ttk.Button(button_frame, text="Forward", command=self.step_forward)
        forward_button.grid(row=0, column=3, padx=5, pady=5)

        reload_button = ttk.Button(button_frame, text="Reload", command=self.reload_simulation)
        reload_button.grid(row=0, column=4, padx=5, pady=5)

        # Speed Slider
        speed_label = ttk.Label(button_frame, text="Set Play Speed (ms):")
        speed_label.grid(row=1, column=0, padx=5, pady=5)

        self.speed_slider = tk.Scale(button_frame, from_=0, to_=1000, orient=tk.HORIZONTAL, command=self.set_speed)
        self.speed_slider.set(self.sSpeed)
        self.speed_slider.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        tabControl.pack(expand=1, fill="both")

    # Simulation control and settings methods
    def set_ring_size(self):
        new_size = simple_input_dialog(self, "Set Ring Size", "Enter new world size:", self.wSize)
        if new_size:
            self.wSize = int(new_size)
            self.worldSize_var.set(f"World Size: {self.wSize}")

    def set_growth(self):
        new_growth = simple_input_dialog(self, "Set Fernies per Turn", "Enter new Fernies per Turn:", self.gpturn)
        if new_growth:
            self.gpturn = int(new_growth)
            self.perTurn_var.set(f"New Fernies per Turn: {self.gpturn}")

    def set_start_ferns(self):
        new_start = simple_input_dialog(self, "Set Starting Fernies", "Enter new Starting Fernies:", self.startcount)
        if new_start:
            self.startcount = int(new_start)
            self.startCLabel_var.set(f"Starting Fernies: {self.startcount}")

    def set_max_soldiers(self):
        new_max = simple_input_dialog(self, "Set Max per Tile", "Enter new Maximum Soldiers per Tile:", self.maxNumSoldiers)
        if new_max:
            self.maxNumSoldiers = int(new_max)
            self.maxSoldiers_var.set(f"Max Fernies per Node: {self.maxNumSoldiers}")

    def set_visibility(self):
        new_vis = simple_input_dialog(self, "Set Visibility Range", "Enter new Visibility Range:", self.visibility_range)
        if new_vis:
            self.visibility_range = int(new_vis)
            self.visRange_var.set(f"Visibility Range: {self.visibility_range}")

    def reload_simulation(self):
        # Logic to reload simulation
        print("Simulation reloaded.")

    def start_simulation(self):
        # Logic to start simulation
        print("Simulation started.")

    def pause_simulation(self):
        # Logic to pause simulation
        print("Simulation paused.")

    def step_forward(self):
        # Logic to step forward in the simulation
        print("Step forward.")

    def step_backward(self):
        # Logic to step backward in the simulation
        print("Step backward.")

    def set_speed(self, value):
        self.sSpeed = int(value)
        print(f"Set speed: {self.sSpeed} ms")


def simple_input_dialog(parent, title, prompt, default_value=""):
    result = tk.simpledialog.askstring(title, prompt, parent=parent, initialvalue=str(default_value))
    return result


if __name__ == "__main__":
    app = COREapp()
    app.mainloop()
