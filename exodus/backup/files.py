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




def compress_files(file_path, backup_dir):
    with ZipFile() as zip_object:
        for folder_name, sub_folders, file_names in os.walk(file_path):
            for filename in file_names:
                file_path = os.path.join(folder_name, filename)
                zip_object.write(file_path, os.path.basename(file_path))



def zip_files_in_directory(directory_path):
     # Get current date and time
    now = datetime.now()
    # Convert to string in the format YYYYMMDDHHMMSS
    date_time_str = now.strftime("%Y%m%d%H%M%S")

    # Create backup directory path with timestamp
    backup_dir = os.path.join(tempfile.gettempdir(), f"E{date_time_str}")
    # Ensure the backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Create a zip file path within the backup directory
    zip_file_path = os.path.join(backup_dir, f"exodus_backup.zip")

    # Create a ZipFile object
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all the files and directories in the given directory
        for foldername, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                # Create the complete file path
                file_path = os.path.join(foldername, filename)
                # Add file to the zip file
                zipf.write(file_path, os.path.relpath(file_path, directory_path))
                print(zip_file_path)
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