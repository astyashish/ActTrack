import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import numpy as np
import os
import sv_ttk
import socket
import threading
import math
from PIL import Image, ImageTk


    
# Define server address and port
SERVER_IP = "127.0.0.1"  # Change to the server's IP address
SERVER_PORT = 52733      # Match the port used in the server

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((SERVER_IP, SERVER_PORT))

print(f"Listening for data on {SERVER_IP}:{SERVER_PORT}...")


class DictManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motion Capture")
        self.root.geometry("900x600")  # Adjusted for better viewing
        sv_ttk.set_theme("dark")  # Apply dark theme (can be toggled to light)
        # Set application icon
        try:
            root.iconbitmap("icon.ico")  # Use the converted .ico file
        except Exception as e:
            print(f"Error setting icon: {e}")


        self.entries = {}
        self.coord = {}  # Initialize the coord dictionary

        # Start a thread to listen for UDP data
        self.stop_udp_thread = False
        self.udp_thread = threading.Thread(target=self.listen_for_udp_data, daemon=True)
        self.udp_thread.start()

        self.saved_dicts = self.load_dicts_from_file()

        # Create main layout
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.sidebar_frame = ttk.Frame(self.main_frame, width=150)
        self.sidebar_frame.pack(side="left", fill="y")

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Sidebar buttons
        ttk.Label(self.sidebar_frame, text="Menu", anchor="center", font=("Arial", 14)).pack(pady=10)

        self.sidebar_buttons = {
            "Manage Capture": self.show_manage_dicts,
            "Settings": self.show_settings,
            "Calculate and Save Angles": self.calculate_and_save_angles,  # New button
            "Auto Save": self.save_dict,
            #"KeyMaping": self.keymaping,
        }
        # Create the timer label
        self.timer_label = ttk.Label(self.root, text="Time left: 0 seconds", font=('Helvetica', 14))
        self.timer_label.pack(pady=20)

        for text, command in self.sidebar_buttons.items():
            button = ttk.Button(self.sidebar_frame, text=text, command=command)
            button.pack(fill="x", pady=5, padx=10)

        self.current_content = None
        self.show_manage_dicts()  # Default view
        # Start the periodic update of coordinates
        self.update_coords()

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle

    def start_timer(self):
        # Function to be called after the timer expires
        # Function to update the timer on the screen every second
        def update_timer(count):
            if count > 0:
                self.timer_label.config(text=f"Time left: {count} seconds")
                # Continue the countdown every second
                threading.Timer(1, update_timer, [count - 1]).start()
                return False
            else:
                return True

        # Set the timer duration in seconds (e.g., 10 seconds)
        timer_duration = 3
        print(f"Timer started for {timer_duration} seconds.")
        # Start the countdown timer
        update_timer(timer_duration)


    def listen_for_udp_data(self):
        """Continuously listen for UDP data and output it to the terminal."""
        while not self.stop_udp_thread:
            try:
                data, addr = client_socket.recvfrom(4096)  # Buffer size of 4096 bytes
                bulkdata=data.decode('utf-8')
                # Initialize entries dictionary
                self.coord = {}

                # Parse the data
                lines = bulkdata.splitlines()  # Split by lines
                for line in lines:
                    if "<EOM>" in line:
                        break  # Stop parsing if end-of-message marker is reached
                    parts = line.split("|")
                    if len(parts) == 4:  # Ensure valid format
                        label_text = int(parts[0])  # Parse label (e.g., 0, 1, ...)
                        x = float(parts[1])  # Parse x value
                        y = float(parts[2])  # Parse y value
                        z = float(parts[3])  # Parse z value

                        # Add or update the respective entry
                        self.coord[label_text] = {"x": x, "y": y, "z": z}
                #print(self.coord[0]["x"])
                #print(f"Data received from {addr}: {data.decode('utf-8')}")
            except Exception as e:
                print(f"Error receiving UDP data: {e}")
                break

    def on_close(self):
        """Handle cleanup when closing the application."""
        self.stop_udp_thread = True  # Signal the UDP thread to stop
        client_socket.close()  # Close the socket
        self.root.destroy()  # Close the GUI

    def clear_content(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_manage_dicts(self):
        """Show the dictionary management UI."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Motion Capture", font=("Arial", 16)).pack(pady=10)

        # Add a scrollable area for the input fields
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Input frame inside the scrollable area
        key = [
            "Nose", "LeftEyeInner", "LeftEye", "LeftEyeOuter", "RightEyeInner", "RightEye",
            "RightEyeOuter", "LeftEar", "RightEar", "MouthLeft", "MouthRight", "LeftShoulder",
            "RightShoulder", "LeftElbow", "RightElbow", "LeftWrist", "RightWrist", "LeftPinky",
            "RightPinky", "LeftIndex", "RightIndex", "LeftThumb", "RightThumb", "LeftHip", "RightHip",
            "LeftKnee", "RightKnee", "LeftAnkle", "RightAnkle", "LeftHeel", "RightHeel", "LeftFootIndex", "RightFootIndex"
        ]

        self.entries = {}
        ttk.Label(scrollable_frame, text="Key").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(scrollable_frame, text="X").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(scrollable_frame, text="Y").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(scrollable_frame, text="Z").grid(row=0, column=3, padx=5, pady=5)
        c=0
    
        for idx, label_text in enumerate(key, start=1):
            ttk.Label(scrollable_frame, text=label_text).grid(row=idx, column=0, padx=5, pady=5)
            # Create StringVars for x, y, z (output values)
            x_var = tk.StringVar(value="0.000")
            y_var = tk.StringVar(value="0.000")
            z_var = tk.StringVar(value="0.000")
            
            x_label = ttk.Label(scrollable_frame, textvariable=x_var, width=10)
            x_label.grid(row=idx, column=1, padx=5, pady=5)
            y_label = ttk.Label(scrollable_frame, textvariable=y_var, width=10)
            y_label.grid(row=idx, column=2, padx=5, pady=5)
            z_label = ttk.Label(scrollable_frame, textvariable=z_var, width=10)
            z_label.grid(row=idx, column=3, padx=5, pady=5)

            self.entries[label_text] = {"x": x_var, "y": y_var, "z": z_var}
            c += 1

        # Buttons for actions
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Save Data", command=self.save_dict).grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="View Data", command=self.view_dicts).grid(row=0, column=1, padx=10)
        ttk.Button(action_frame, text="Delete Data", command=self.delete_dict).grid(row=0, column=2, padx=10)


    def calculate_and_save_angles(self):
        # recent data
        last_dict_name = list(self.saved_dicts.keys())[-1]
        """Calculate and save angles for multiple joints to the angles.json file."""

        dict_name = simpledialog.askstring("Enter Data Name", "Enter a name for the Data:")

        if dict_name not in self.saved_dicts:
            messagebox.showerror("Error", f"Dictionary '{dict_name}' not found.")
            return

        points = self.saved_dicts[dict_name]

        # Validate the points to ensure they contain valid float values
        point_list = {}
        for k, v in points.items():
            try:
                # Only process the entries that have values
                if v.get('x') and v.get('y') and v.get('z'):
                    x = float(v['x'])
                    y = float(v['y'])
                    z = float(v['z'])

                    point_list[k] = (x, y, z)
            except ValueError:
                messagebox.showerror("Error", f"Invalid data in point '{k}': {v}")
                return

        # Define the joints for which angles need to be calculated
        joint_definitions = {
            'LeftElbow': ['LeftShoulder', 'LeftElbow', 'LeftWrist'],        # Left Elbow
            'RightElbow': ['RightShoulder', 'RightElbow', 'RightWrist'],    # Right Elbow
            'LeftShoulder': ['LeftHip', 'LeftShoulder', 'LeftElbow'],       # Left Shoulder
            'RightShoulder': ['RightHip', 'RightShoulder', 'RightElbow'],   # Right Shoulder
            'LeftHip': ['LeftShoulder', 'LeftHip', 'LeftKnee'],             # Left Hip
            'RightHip': ['RightShoulder', 'RightHip', 'RightKnee'],         # Right Hip
            'LeftKnee': ['LeftHip', 'LeftKnee', 'LeftAnkle'],               # Left Knee
            'RightKnee': ['RightHip', 'RightKnee', 'RightAnkle'],           # Right Knee
            'LeftAnkle': ['LeftKnee', 'LeftAnkle', 'LeftFootIndex'],        # Left Ankle
            'RightAnkle': ['RightKnee', 'RightAnkle', 'RightFootIndex'],    # Right Ankle
            'HeadAngle': ['LeftShoulder', 'RightShoulder', 'Nose'],         # Head Angle (Special case)
        }

        angles = {}

        # Calculate angles for each joint
        try:
            for joint_name, joint_points in joint_definitions.items():
                # For 'HeadAngle', use the special function
                if joint_name == 'HeadAngle':
                    if all(point_list.get(p) for p in joint_points):
                        # Unpack the points into individual variables
                        left_shoulder = point_list[joint_points[0]]
                        right_shoulder = point_list[joint_points[1]]
                        nose = point_list[joint_points[2]]
                        
                        # Call the head angle calculation function with individual arguments
                        head_angle = self.calculate_head_angle_from_vectors(left_shoulder, right_shoulder, nose)
                        angles[joint_name] = head_angle+20
                    else:
                        angles[joint_name] = None  # Mark as None if data is missing
                else:
                    if all(point_list.get(p) for p in joint_points):
                        p1, p2, p3 = (point_list[joint_points[0]], 
                                    point_list[joint_points[1]], 
                                    point_list[joint_points[2]])
                        angle = self.calculate_angle(p1, p2, p3)
                        angles[joint_name] = angle
                    else:
                        angles[joint_name] = None  # Mark as None if data is missing

            # Save the angles to angles.json
            self.save_angles_to_file(dict_name, angles)
            messagebox.showinfo("Success", f"Angles calculated and saved: {angles}")
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating angles: {e}")

    @staticmethod
    def calculate_head_angle_from_vectors(left_shoulder, right_shoulder, nose):
        """
        Calculate the head angle between the shoulders and the nose based on their vectors.
        The angle is calculated using the dot product of the shoulder vector and the nose vector.

        Parameters:
        - left_shoulder: (x, y) coordinates of the left shoulder.
        - right_shoulder: (x, y) coordinates of the right shoulder.
        - nose: (x, y) coordinates of the nose.

        Returns:
        - The head angle in degrees.
        """
        # Calculate the vector between the shoulders
        shoulder_vector =  [right_shoulder[0] - left_shoulder[0], right_shoulder[1] - left_shoulder[1]]  # Vector between shoulders        
        # Calculate the vector from the midpoint of the shoulders to the nose
        nose_vector = [nose[0] - (left_shoulder[0] + right_shoulder[0]) / 2, nose[1] - (left_shoulder[1] + right_shoulder[1]) / 2]  # Vector from the midpoint of shoulders to the nose

        # Calculate the dot product of the two vectors
        dot_product = shoulder_vector[0] * nose_vector[0] + shoulder_vector[1] * nose_vector[1]
        
        # Calculate the magnitude (length) of both vectors
        magnitude_shoulder = (shoulder_vector[0]**2 + shoulder_vector[1]**2)**0.5
        magnitude_nose = (nose_vector[0]**2 + nose_vector[1]**2)**0.5
        
        # Calculate the angle in radians
        angle_radians = math.acos(dot_product / (magnitude_shoulder * magnitude_nose))
        
        # Convert the angle to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees



    def save_angles_to_file(self, dict_name, angles):
        """Save the calculated angle to the angles.json file."""
        
        angle_data = {dict_name: angles}

        # Load existing angles or initialize an empty list
        if os.path.exists("angles.json"):
            with open("angles.json", "r") as file:
                angles_data = json.load(file)
        else:
            angles_data = []

        # Add the new angle to the data
        angles_data.append(angle_data)

        # Save the updated angle data to angles.json
        with open("angles.json", "w") as file:
            json.dump(angles_data, file, indent=4)
##---------------------with timer  -------------------------------------------
    def start_timer(self, callback):
        """Start the timer, and then call the callback function after the timer ends."""
        def update_timer(count):
            if count > 0:
                self.timer_label.config(text=f"Time left: {count} seconds")
                threading.Timer(1, update_timer, [count - 1]).start()
            else:
                callback()

        # Set the timer duration in seconds (e.g., 5 seconds for this example)
        timer_duration = 5
        self.timer_label = ttk.Label(self.root, text=f"Time left: {timer_duration} seconds", font=('Helvetica', 14))
        self.timer_label.pack(pady=20)

        update_timer(timer_duration)

    def save_dict(self):
        """Save the dictionary with a user-defined name after a timer."""
        dict_name = simpledialog.askstring("Save Data", "Enter a name for this Data:")
        if not dict_name:
            messagebox.showerror("Error", "Data name cannot be empty!")
            return
        
        # Start the timer, and only save after the timer ends
        self.start_timer(lambda: self._save_dict_after_timer(dict_name))

    def _save_dict_after_timer(self, dict_name):
        """This function will save the dictionary after the timer ends."""
        # Example of creating a new dictionary (you should update this as per your requirement)
        new_dict = {
            key: {
                "x": entry["x"].get(),
                "y": entry["y"].get(),
                "z": entry["z"].get(),
            }
            for key, entry in self.entries.items()
        }

        if dict_name in self.saved_dicts:
            overwrite = messagebox.askyesno("Overwrite?", f"A Data named '{dict_name}' already exists. Overwrite?")
            if not overwrite:
                return

        # Save the dictionary
        self.saved_dicts[dict_name] = new_dict
        self.save_dicts_to_file()

        messagebox.showinfo("Success", f"Data '{dict_name}' saved successfully.")
#--------------
    def show_settings(self):
            """Show the settings UI."""
            self.clear_content()
            ttk.Label(self.content_frame, text="Settings", font=("Arial", 16)).pack(pady=10)
    def load_dicts_from_file(self):
        """Load dictionaries from a JSON file."""
        if os.path.exists("saved_dicts.json"):
            with open("saved_dicts.json", "r") as file:
                return json.load(file)
        return {}
    def update_coords(self):
            """Update coordinates periodically to show real-time values."""
            # Assuming `self.coord` contains the coordinates for the body parts
            for idx, label_text in enumerate(self.entries.keys()):
                # Update x, y, z values in real-time from `self.coord`
                coord = self.coord.get(idx, {"x": "0.000", "y": "0.000", "z": "0.000"})
                self.entries[label_text]["x"].set(coord.get("x", "0.000"))
                self.entries[label_text]["y"].set(coord.get("y", "0.000"))
                self.entries[label_text]["z"].set(coord.get("z", "0.000"))

            # Refresh every 100 milliseconds
            self.root.after(100, self.update_coords)
    def save_dicts_to_file(self):
        """Save dictionaries to a JSON file."""
        with open("saved_dicts.json", "w") as file:
            json.dump(self.saved_dicts, file, indent=4)

    def view_dicts(self):
        """View all saved dictionaries."""
        self.clear_content()

        ttk.Label(self.content_frame, text="Saved Data", font=("Arial", 16)).pack(pady=10)

        for dict_name in self.saved_dicts.keys():
            ttk.Label(self.content_frame, text=dict_name).pack(pady=5)

    def delete_dict(self):
        """Delete a dictionary."""
        dict_name = simpledialog.askstring("Delete Data", "Enter the Data name to delete:")
        if dict_name in self.saved_dicts:
            del self.saved_dicts[dict_name]
            self.save_dicts_to_file()
            messagebox.showinfo("Success", f"Data '{dict_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"Dictionary '{dict_name}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictManagerApp(root)
    app.show_manage_dicts()
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # Ensure proper cleanup on close
    root.mainloop()
