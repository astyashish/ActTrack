import tkinter as tk
from tkinter import ttk
import sv_ttk  # type: ignore
import json
from pathlib import Path
import global_vars
import subprocess  # Used to run the executable

# Sample data for angle.json (if it doesn't exist)
SAMPLE_DATA = {
}


    
class ModernDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Debug Dashboard")
        self.root.geometry("1000x700")
        sv_ttk.set_theme("light")  # Apply dark theme (can be toggled to light)


        # Title Label
        title_label = ttk.Label(root, text="Advanced Debug Dashboard", font=("Arial", 24))
        title_label.pack(pady=10)

        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Debug Table
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Debug Table")
        self.create_debug_tab()

        # Tab 2: Settings
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Settings")
        self.create_settings_tab()

        # Tab 3: Logs
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Logs")
        self.create_logs_tab()

        # Tab 6: Games
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="Games")
        self.create_game_window(self.tab4)


    def create_debug_tab(self):
        """Setup contents for the Debug Table tab."""
        table_frame = ttk.Frame(self.tab1)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Debug Table
        self.tree = ttk.Treeview(
            table_frame,
            columns=("Property", "Value"),
            show="headings",
            height=15,
        )
        self.tree.pack(fill="both", expand=True)

        # Define Columns
        self.tree.heading("Property", text="Property")
        self.tree.heading("Value", text="Value")

        # Populate Table
        self.refresh_table()

        # Refresh Button
        refresh_button = ttk.Button(
            self.tab1, text="Refresh Table", command=self.refresh_table
        )
        refresh_button.pack(pady=10)

    def create_settings_tab(self):
        """Setup contents for the Settings tab."""
        settings_frame = ttk.Frame(self.tab2)
        settings_frame.pack(pady=10, padx=10, fill="both", expand=True)
                # Create the button that runs a Python script
        game_name_label = ttk.Label(settings_frame, text="Data Capture(Dataset)", font=("Arial", 14))
        game_name_label.pack(pady=20)
        start_button = ttk.Button(
            settings_frame, 
            text="Data Capture", 
            command=lambda: self.run_python_script("Data_Capture.py")
        )
        start_button.pack(pady=20)

        # Sliders Section
        slider_label = ttk.Label(settings_frame, text="Adjust Settings", font=("Arial", 16))
        slider_label.pack(pady=10)

        slider1 = ttk.Scale(settings_frame, from_=0, to=100, orient="horizontal")
        slider1.pack(pady=5, padx=20, fill="x")
        slider1_label = ttk.Label(settings_frame, text="Slider 1: Value = 50")
        slider1_label.pack()

        def update_slider1_label(val):
            slider1_label.config(text=f"Slider 1: Value = {int(float(val))}")

        slider1.config(command=update_slider1_label)

        slider2 = ttk.Scale(settings_frame, from_=1, to=10, orient="horizontal")
        slider2.pack(pady=5, padx=20, fill="x")
        slider2_label = ttk.Label(settings_frame, text="Slider 2: Value = 5")
        slider2_label.pack()

        def update_slider2_label(val):
            slider2_label.config(text=f"Slider 2: Value = {float(val):.1f}")

        slider2.config(command=update_slider2_label)

        # Advanced Settings Section
        adv_label = ttk.Label(settings_frame, text="Advanced Options", font=("Arial", 16))
        adv_label.pack(pady=20)

        checkbox_frame = ttk.Frame(settings_frame)
        checkbox_frame.pack(pady=10)

        self.checkbox1_state = tk.BooleanVar(value=True)
        def toggle_debug():
            global_vars.DEBUG_GUI = self.checkbox1_state.get()


        checkbox1 = ttk.Checkbutton(
            checkbox_frame,
        text="DEBUG",
        variable=self.checkbox1_state,
        command=toggle_debug

        )

        checkbox1.pack(side="left", padx=10)

        self.checkbox2_state = tk.BooleanVar(value=False)

        def switch_camera():
            global_vars.CAM_INDEX = 1 if self.checkbox2_state.get() else 0

        checkbox2 = ttk.Checkbutton(
            checkbox_frame, text="Switch Camera", variable=self.checkbox2_state, command=switch_camera
        )
        checkbox2.pack(side="left", padx=10)
    def create_logs_tab(self):
        """Setup contents for the Logs tab."""
        logs_frame = ttk.Frame(self.tab3)
        logs_frame.pack(pady=10, padx=10, fill="both", expand=True)

        logs_label = ttk.Label(logs_frame, text="Logs", font=("Arial", 16))
        logs_label.pack(pady=10)

        # Textbox for logs
        self.logs_text = tk.Text(logs_frame, wrap="word", height=20)
        self.logs_text.pack(pady=5, padx=10, fill="both", expand=True)

        # Add sample log
        self.logs_text.insert("end", "System initialized.\n")
        self.logs_text.insert("end", "Debugging enabled.\n")

        # Add Clear Logs Button
        clear_button = ttk.Button(logs_frame, text="Clear Logs", command=self.clear_logs)
        clear_button.pack(pady=10)

    def run_python_script(self, script_name):
        """Function to run a Python script when the button is clicked."""
        try:
            # Run the Python script using subprocess
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running {script_name}: {e}")
        except FileNotFoundError:
            print(f"Error: {script_name} not found. Please check the script path.")

    def run_body_tracking(self, event=None):
        """Function to run the BodyTrackingAlpha.exe when the button is clicked"""
        try:
            # Running the executable
            subprocess.run(["D:\\Advance Body_Tracker\\Test\\BodyTrackingAlpha.exe"], check=True)
            #print("BodyTrackingAlpha.exe started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error while starting BodyTrackingAlpha.exe: {e}")
        except FileNotFoundError:
            print("Error: BodyTrackingAlpha.exe not found. Please ensure the file is in the correct directory.")

    def test(self, event=None):
        """Function to run the BodyTrackingAlpha.exe when the button is clicked"""
        try:
            # Specify arguments if windowed mode is supported
            subprocess.run(["BodyTrackingAlpha.exe"], check=True)
            # Add '--windowed' or any appropriate argument if supported by the exe
        except subprocess.CalledProcessError as e:
            print(f"Error while starting BodyTrackingAlpha.exe: {e}")
        except FileNotFoundError:
            print("Error: BodyTrackingAlpha.exe not found. Please ensure the file is in the correct directory.")


    def create_game_window(self, tab):
        """Function to create a window with a button and game name label."""
        # Create and place the label displaying the game name
        keymap_frame = ttk.Frame(tab)
        keymap_frame.pack(pady=10, padx=10, fill="both", expand=True)

        game_name_label = ttk.Label(keymap_frame, text="Body Tracking Game", font=("Arial", 14))
        game_name_label.pack(pady=20)

        # Create the button that runs the BodyTrackingAlpha.exe
        start_button = ttk.Button(keymap_frame, text="Start Body Tracking", command=self.run_body_tracking)
        start_button.pack(pady=20)

        game_name_label = ttk.Label(keymap_frame, text="Test MoCap", font=("Arial", 14))
        game_name_label.pack(pady=20)

        # Create the button that runs the BodyTrackingAlpha.exe
        start_button = ttk.Button(keymap_frame, text="Test MoCap", command=self.test)
        start_button.pack(pady=20)


    def save_json(self):
        with open("key.json", "w") as file:
            json.dump(self.data, file, indent=4)
    def save_keymapping(self, dict_name):
        """Save the user input back to the JSON file."""
        updated_dict = {}
        for key, entry in self.entries.items():
            updated_dict[key] = entry.get()

        self.data[dict_name] = updated_dict
        self.save_json(self.data)
        tk.messagebox.showinfo("Success", f"Key Mapping for {dict_name} saved!")

    def refresh_table(self):
        """Refresh the data in the Debug Table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add global variable data to table (replace with your actual data)
        data = [
            ("CHECKBOX_STATE", True),
            ("DEBUG_MODE", False),
            ("FPS", 30),
            ("WIDTH", 1920),
            ("HEIGHT", 1080),
            ("MODEL_COMPLEXITY", 1),
        ]
        for prop, value in data:
            self.tree.insert("", "end", values=(prop, value))

    def clear_logs(self):
        """Clear the logs."""
        self.logs_text.delete("1.0", "end")


# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDashboard(root)
    root.mainloop()
