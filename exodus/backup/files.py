import os
import shutil
import tempfile
import zipfile
from zipfile import ZipFile
from datetime import datetime

def backup_files(file_paths, backup_dir):
    """
    Backs up a list of files and directories to a specified backup directory.

    Args:
        file_paths (list): A list of file or directory paths to back up.
        backup_dir (str): The directory where backups will be stored.
    """
    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Loop through each file or directory path in the list
    for file_path in file_paths:
        if os.path.exists(file_path):
            # If it's a file, copy it to the backup directory
            if os.path.isfile(file_path):
                shutil.copy(file_path, backup_dir)
                print(f"File {file_path} backed up to {backup_dir}.")
            # If it's a directory, copy the entire directory
            elif os.path.isdir(file_path):
                # Determine the target path in the backup directory
                target_dir = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.copytree(file_path, target_dir)
                print(f"Directory {file_path} backed up to {target_dir}.")
        else:
            print(f"File or directory {file_path} not found.")


def zip_files_in_directory(directory_path):
    # Get current date and time
    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d%H%M%S")

    # Get the system's temporary directory
    temp_dir = tempfile.gettempdir()

    # Create a unique directory within the temporary directory
    backup_dir = os.path.join(temp_dir, f"E{date_time_str}")
    os.makedirs(backup_dir, exist_ok=True)

    # Create a ZIP file path
    zip_file_path = os.path.join(backup_dir, "edeparture.zip")

    # Create the ZIP file
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, _, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))
                print(f"Added to ZIP: {file_path}")

    return zip_file_path


def store_backup_in_temp_dir(backup_file):
    """
    Moves the provided backup file to the system's temporary directory.

    Args:
        backup_file (str): The path to the backup file to be stored in the temp directory.

    Returns:
        str: The full path to the stored backup file in the temp directory.
    """

    # Get the system's temporary directory
    temp_dir = tempfile.gettempdir()

    # Get the base name of the backup file
    backup_filename = os.path.basename(backup_file)

    # Define the new path in the temporary directory
    temp_backup_path = os.path.join(temp_dir, backup_filename)

    try:
        # Move the backup file to the temporary directory
        shutil.move(backup_file, temp_backup_path)
        print(f"Backup file successfully moved to: {temp_backup_path}")
    except FileNotFoundError:
        print(f"Error: The file {backup_file} does not exist.")
    except PermissionError:
        print(f"Error: Insufficient permissions to move the file to {temp_dir}.")
    except Exception as e:
        print(f"An error occurred while moving the file: {e}")
    
    return temp_backup_path
