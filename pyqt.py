import customtkinter as ctk
import json
from pathlib import Path
import global_vars
import subprocess  # Used to run the executable
from PIL import Image
import socket
import platform
# Sample data for angle.json (if it doesn't exist)
SAMPLE_DATA = {}
# Get the hostname (desktop name)
hostname = socket.gethostname()

# Get the local IP address (network name)
ip_address = socket.gethostbyname(hostname)
system_info = platform.uname()

class ModernDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Debug Dashboard")
        self.root.geometry("1000x700")
        ctk.set_appearance_mode("dark")  # Set appearance mode
        ctk.set_default_color_theme("dark-blue")  # Set color theme

        # Title Label
        title_label = ctk.CTkLabel(root, text="Advanced Debug Dashboard", font=("Arial", 24))
        title_label.pack(pady=10)

        # Hamburger Menu Button
        self.sidebar_visible = False
        menu_button = ctk.CTkButton(
            root, text="☰", width=40, command=self.toggle_sidebar
        )
        menu_button.place(x=10, y=10)

        # Create Sidebar
        self.sidebar = self.create_sidebar()

        # Create Notebook for Tabs
        self.notebook = ctk.CTkTabview(root, width=950, height=650)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Debug Table
        self.tab1 = self.notebook.add("Debug Table")
        self.create_debug_tab()

        # Tab 2: Settings
        self.tab2 = self.notebook.add("Settings")
        self.create_settings_tab()

        # Tab 3: Logs
        self.tab3 = self.notebook.add("Logs")
        self.create_logs_tab()

        # Tab 4: Games
        self.tab4 = self.notebook.add("Games")
        self.create_game_window(self.tab4)




    def create_debug_tab(self):
        """Setup contents for the Debug Table tab."""
        table_frame = ctk.CTkFrame(self.tab1)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Debug Table
        self.tree = ctk.CTkTextbox(table_frame, height=400, font=("Arial", 12))
        self.tree.pack(fill="both", expand=True)

        # Populate Table
        self.refresh_table()

        # Refresh Button
        refresh_button = ctk.CTkButton(
            self.tab1, text="Refresh Table", command=self.refresh_table
        )
        refresh_button.pack(pady=10)
    def keymap(self):
        keymap_window = ctk.CTkToplevel(self.root)  # Create a new top-level window
        keymap_window.title("Keymap")
        keymap_window.geometry("400x300")  # Set the size of the popup

        # Create the "Create Keymap" button
        create_button = ctk.CTkButton(
            keymap_window,
            text="Create Keymap",
            command=self.open_create_keymap_popup
        )
        create_button.pack(pady=20)

    def open_create_keymap_popup(self):
        """Open a popup window to create a new keymap."""
        popup = ctk.CTkToplevel(self.root)
        popup.title("Create Keymap")
        popup.geometry("400x300")

        # Popup content
        label = ctk.CTkLabel(popup, text="Create your keymap here", font=("Arial", 16))
        label.pack(pady=20)

        entry = ctk.CTkEntry(popup, placeholder_text="Enter keymap details...")
        entry.pack(pady=10, padx=20, fill="x")

        save_button = ctk.CTkButton(popup, text="Save", command=popup.destroy)
        save_button.pack(pady=20)
    def create_settings_tab(self):
        """Setup contents for the Settings tab."""
        settings_frame = ctk.CTkFrame(self.tab2)
        settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Data Capture Button
        game_name_label = ctk.CTkLabel(settings_frame, text="Data Capture (Dataset)", font=("Arial", 14))
        game_name_label.pack(pady=20)
        start_button = ctk.CTkButton(
            settings_frame, 
            text="Data Capture", 
            command=lambda: self.run_python_script("Data_Capture.py")
        )
        start_button.pack(pady=20)

        # Sliders Section
        slider_label = ctk.CTkLabel(settings_frame, text="Adjust Settings", font=("Arial", 16))
        slider_label.pack(pady=10)

        slider1 = ctk.CTkSlider(settings_frame, from_=0, to=100)
        slider1.pack(pady=5, padx=20, fill="x")
        slider1_label = ctk.CTkLabel(settings_frame, text="Slider 1: Value = 50")
        slider1_label.pack()

        def update_slider1_label(val):
            slider1_label.configure(text=f"Slider 1: Value = {int(val)}")

        slider1.configure(command=update_slider1_label)

        slider2 = ctk.CTkSlider(settings_frame, from_=1, to=10, number_of_steps=9)
        slider2.pack(pady=5, padx=20, fill="x")
        slider2_label = ctk.CTkLabel(settings_frame, text="Slider 2: Value = 5")
        slider2_label.pack()

        def update_slider2_label(val):
            slider2_label.configure(text=f"Slider 2: Value = {float(val):.1f}")

        slider2.configure(command=update_slider2_label)

        # Advanced Settings Section
        adv_label = ctk.CTkLabel(settings_frame, text="Advanced Options", font=("Arial", 16))
        adv_label.pack(pady=20)

        checkbox_frame = ctk.CTkFrame(settings_frame)
        checkbox_frame.pack(pady=10)

        self.checkbox1_state = ctk.BooleanVar(value=True)
        checkbox1 = ctk.CTkCheckBox(
            checkbox_frame,
            text="DEBUG",
            variable=self.checkbox1_state,
            command=lambda: setattr(global_vars, 'DEBUG_GUI', self.checkbox1_state.get())
        )
        checkbox1.pack(side="left", padx=10)

        self.checkbox2_state = ctk.BooleanVar(value=False)
        checkbox2 = ctk.CTkCheckBox(
            checkbox_frame, 
            text="Switch Camera", 
            variable=self.checkbox2_state, 
            command=lambda: setattr(global_vars, 'CAM_INDEX', 1 if self.checkbox2_state.get() else 0)
        )
        checkbox2.pack(side="left", padx=10)

    def create_logs_tab(self):
        """Setup contents for the Logs tab."""
        logs_frame = ctk.CTkFrame(self.tab3)
        logs_frame.pack(pady=10, padx=10, fill="both", expand=True)

        logs_label = ctk.CTkLabel(logs_frame, text="Logs", font=("Arial", 16))
        logs_label.pack(pady=10)

        # Textbox for logs
        self.logs_text = ctk.CTkTextbox(logs_frame, wrap="word", height=20)
        self.logs_text.pack(pady=5, padx=10, fill="both", expand=True)

        # Add sample log
        self.logs_text.insert("end", "System initialized.\n")
        self.logs_text.insert("end", "Debugging enabled.\n")

        # Add Clear Logs Button
        clear_button = ctk.CTkButton(logs_frame, text="Clear Logs", command=self.clear_logs)
        clear_button.pack(pady=10)

    def create_game_window(self, tab):
        """Function to create a window with a button and game name label."""
        keymap_frame = ctk.CTkFrame(tab)
        keymap_frame.pack(pady=10, padx=10, fill="both", expand=True)

        game_name_label = ctk.CTkLabel(keymap_frame, text="Body Tracking Game", font=("Arial", 14))
        game_name_label.pack(pady=20)

        # Start Body Tracking Button
        start_button = ctk.CTkButton(keymap_frame, text="Start Body Tracking", command=self.run_body_tracking)
        start_button.pack(pady=20)

        game_name_label = ctk.CTkLabel(keymap_frame, text="Test MoCap", font=("Arial", 14))
        game_name_label.pack(pady=20)

        # Test MoCap Button
        test_button = ctk.CTkButton(keymap_frame, text="Test MoCap", command=self.test)
        test_button.pack(pady=20)
    def create_sidebar(self):
        """Create the sidebar UI elements."""
        sidebar = ctk.CTkFrame(self.root, width=250, height=700, corner_radius=13, bg_color="transparent")

        # User Info Section
        try:
            user_image_raw = Image.open("icon.jpg").resize((80, 80))  # Replace with actual image path
        except FileNotFoundError:
            print("Warning: 'icon.jpg' not found. Using a placeholder.")
            user_image_raw = Image.new('RGB', (80, 80), color='gray')  # Placeholder image

        user_image = ctk.CTkImage(user_image_raw, size=(80, 80))

        user_photo = ctk.CTkLabel(sidebar, image=user_image,text="")
        user_photo.image = user_image  # Prevent garbage collection
        user_photo.pack(pady=20)

        user_name_label = ctk.CTkLabel(sidebar, text=hostname, font=("Arial", 16))
        user_name_label.pack(pady=10)

        pc_label = ctk.CTkLabel(sidebar, text=ip_address, font=("Arial", 12))
        pc_label.pack(pady=5)


        # Buttons Section
        button_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        button_frame.pack(padx=30,pady=30, fill="both", expand=True)

        self.create_sidebar_button(button_frame, "Dashboard", self.dashboard_action,180,40)
        self.create_sidebar_button(button_frame, "Keymap", self.keymap,180,40)
        self.create_sidebar_button(button_frame, "Logs", self.logs_action,180,40)
        self.create_sidebar_button(button_frame, "Logout", self.logout_action,180,40)

        return sidebar

    def create_sidebar_button(self, frame, text, command,width,height):
        """Helper function to create sidebar buttons with enhanced styling."""
        button = ctk.CTkButton(
            frame, 
            text=text, 
            command=command, 
            width=width,
            height=height,
            corner_radius=15, 
            font=("Arial", 14), 
            fg_color="#0078D7",  # Modern blue color
            hover_color="#0056A8",  # Slightly darker blue for hover
            text_color="white"
        )
        button.pack(pady=15, padx=10)

    def toggle_sidebar(self):
        """Show or hide the sidebar."""
        if self.sidebar_visible:
            self.sidebar.place_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.place(x=0, y=45)
            self.sidebar.lift()  # Bring the sidebar to the front
            self.sidebar_visible = True
    # Button actions
    def dashboard_action(self):
        """Action for Dashboard button."""
        print("Dashboard button clicked.")

    def settings_action(self):
        """Action for Settings button."""
        print("Settings button clicked.")

    def logs_action(self):
        """Action for Logs button."""
        print("Logs button clicked.")

    def logout_action(self):
        """Action for Logout button."""
        print("Logout button clicked.")

    def run_python_script(self, script_name):
        """Function to run a Python script when the button is clicked."""
        try:
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running {script_name}: {e}")
        except FileNotFoundError:
            print(f"Error: {script_name} not found. Please check the script path.")

    def run_body_tracking(self):
        """Function to run the BodyTrackingAlpha.exe."""
        try:
            subprocess.run(["D:\\Advance Body_Tracker\\Test\\BodyTrackingAlpha.exe"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while starting BodyTrackingAlpha.exe: {e}")
        except FileNotFoundError:
            print("Error: BodyTrackingAlpha.exe not found. Ensure the file is in the correct directory.")

    def test(self):
        """Function to test motion capture."""
        try:
            subprocess.run(["BodyTrackingAlpha.exe"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while starting BodyTrackingAlpha.exe: {e}")
        except FileNotFoundError:
            print("Error: BodyTrackingAlpha.exe not found. Ensure the file is in the correct directory.")

    def refresh_table(self):
        """Refresh the data in the Debug Table."""
        data = [
            ("CHECKBOX_STATE", True),
            ("DEBUG_MODE", False),
            ("FPS", 30),
            ("WIDTH", 1920),
            ("HEIGHT", 1080),
            ("MODEL_COMPLEXITY", 1),
        ]

        self.tree.delete("1.0", "end")
        for prop, value in data:
            self.tree.insert("end", f"{prop}: {value}\n")

    def clear_logs(self):
        """Clear the logs."""
        self.logs_text.delete("1.0", "end")

# Main Execution
if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernDashboard(root)
    root.mainloop()
