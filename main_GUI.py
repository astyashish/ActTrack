from body import BodyThread
import time
import global_vars
from gui import ModernDashboard
import tkinter as tk


import os
from PIL import Image, ImageTk # type: ignore

# Change working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def show_splash():
    """Display a splash screen with a logo."""
    splash = tk.Toplevel()
    splash.geometry("900x900")  # Set splash window dimensions
    splash.title("ActTrack")
    
    # Load the logo using Pillow
    try:
        logo_image = Image.open("icon.jpg")  # Path to your .jpg file
        logo = ImageTk.PhotoImage(logo_image)
    except Exception as e:
        print(f"Error loading splash image: {e}")
        # Show a text-only splash instead
        label = tk.Label(splash, text="ActTrack\nAdvanced Body Tracker", font=("Arial", 32), pady=50)
        label.pack(expand=True)
        splash.after(2000, splash.destroy)
        return
    
    # Add the logo to a label
    label = tk.Label(splash, image=logo)
    label.image = logo  # Keep a reference to prevent garbage collection
    label.pack()

    # Auto-close splash after 2 seconds
    splash.after(2000, splash.destroy)


def main():
    # Initialize the root Tk window
    root = tk.Tk()
    root.withdraw()  # Hide the root window during splash

    # Show the splash screen
    show_splash()

    # Wait for the splash screen to close
    root.after(2100, lambda: root.deiconify())  # Unhide root after splash

    # Set application icon
    try:
        root.iconbitmap("icon.ico")  # Use the converted .ico file
    except Exception as e:
        print(f"Error setting icon: {e}")

    # Start the BodyThread
    thread = BodyThread()
    thread.start()

    # Launch the GUI
    app = ModernDashboard(root)
    root.mainloop()

    # Cleanup after the application exits
    print("Exiting…")
    global_vars.KILL_THREADS = True
    time.sleep(0.5)
    exit()


if __name__ == "__main__":
    main()
