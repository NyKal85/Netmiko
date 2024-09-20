import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.simpledialog import askstring


# Function to check if all strings are present in a text file and identify missing strings
def check_file(file_path, strings_to_check):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    missing_strings = []

    # Check if each string is present in any line
    for string in strings_to_check:
        found = any(string in line for line in lines)
        if not found:
            missing_strings.append(string)

    return missing_strings


# Function to select the folder and check files
def select_folder_and_check():
    # Ask for the folder containing text files
    folder_path = filedialog.askdirectory(title="Select Folder Containing Text Files")

    if folder_path:
        # Ask for the strings to check (comma-separated)
        strings_input = askstring("Input Strings", "Enter the strings to check for (comma-separated):")

        if strings_input:
            # Convert the user input into a list of strings
            strings_to_check = [s.strip() for s in strings_input.split(",")]

            # Store information about bad files and their missing strings
            bad_files = {}

            # Loop through all the text files in the directory
            for filename in os.listdir(folder_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(folder_path, filename)
                    missing_strings = check_file(file_path, strings_to_check)

                    # If there are missing strings, store the file and its missing strings
                    if missing_strings:
                        bad_files[filename] = missing_strings

            # Create a more human-readable output and write to a file
            with open('results.txt', 'w', encoding='utf-8') as result_file:
                if bad_files:
                    result_file.write("Bad files and missing strings:\n")
                    for file, missing in bad_files.items():
                        result_file.write(f"\nFile: {file}\n")
                        result_file.write(f"Missing strings: {', '.join(missing)}\n")
                        result_file.write("-" * 40 + "\n")
                else:
                    result_file.write("All files are good. No strings are missing.\n")

            # Notify the user that the result has been saved
            messagebox.showinfo("Results", "Check the 'results.txt' file for details on missing strings.")


# Main program
if __name__ == "__main__":
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show the folder selection and string input dialogs
    select_folder_and_check()

