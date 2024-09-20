import os
import json
import tkinter as tk
from tkinter import filedialog

# File to store the selected directory path
config_file = "folder_config.json"

def select_directory():
    """ Opens file explorer for user to select folder and returns the path. """
    root = tk.Tk()
    root.withdraw()  # Hides the root window
    folder_path = filedialog.askdirectory()  # Open file explorer
    return folder_path

def load_saved_directory():
    """ Loads the saved directory path from config file if it exists. """
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            return config.get("folder_path", None)
    return None

def save_directory(folder_path):
    """ Saves the selected directory path to the config file. """
    with open(config_file, "w") as file:
        json.dump({"folder_path": folder_path}, file)

def get_save_directory():
    """ 
    Retrieves the save directory, opens file explorer if needed, 
    and saves the path for future use.
    """
    folder_path = load_saved_directory()

    # If no folder is saved or folder doesn't exist, ask the user to select one
    if not folder_path or not os.path.exists(folder_path):
        folder_path = select_directory()
        if folder_path:
            save_directory(folder_path)
        else:
            print("No folder selected. Exiting.")
            exit(1)

    return folder_path

# Example usage
save_folder = get_save_directory()
print(f"Files will be saved to: {save_folder}")

# Now you can use 'save_folder' to output files

