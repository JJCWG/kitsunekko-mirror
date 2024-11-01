import os
import re

# Define Windows' invalid characters for file and folder names
INVALID_CHARS = r'[<>:"/\\|?*]'
RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                  "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}

def sanitize_name(name, is_folder=False):
    # Replace invalid characters with underscores
    name = re.sub(INVALID_CHARS, "_", name)
    
    # Additional step for folders: Replace all periods with underscores
    if is_folder:
        name = name.replace(".", "_")

    # Check for reserved names and add an underscore if necessary
    if name.upper() in RESERVED_NAMES:
        name += "_"
    return name

def rename_invalid_files_folders(root_dir):
    # Walk through all directories and files starting from root_dir
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Rename files
        for filename in files:
            sanitized_name = sanitize_name(filename, is_folder=False)
            if filename != sanitized_name:
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, sanitized_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed file: '{old_path}' -> '{new_path}'")
                except Exception as e:
                    print(f"Failed to rename file '{old_path}': {e}")

        # Rename directories
        for dirname in dirs:
            sanitized_name = sanitize_name(dirname, is_folder=True)
            if dirname != sanitized_name:
                old_path = os.path.join(root, dirname)
                new_path = os.path.join(root, sanitized_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed folder: '{old_path}' -> '{new_path}'")
                except Exception as e:
                    print(f"Failed to rename folder '{old_path}': {e}")

# Start from the directory where the script is located
current_directory = os.path.dirname(os.path.abspath(__file__))
rename_invalid_files_folders(current_directory)

