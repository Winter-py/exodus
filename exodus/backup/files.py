import os
import shutil
import tempfile
from zipfile import ZipFile

def backup_files(file_paths, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            shutil.copy(file_path, backup_dir)
        else:
            print(f"File {file_path} not found.")



def compress_files(file_path, backup_dir):
    with ZipFile() as zip_object:
        for folder_name, sub_folders, file_names in os.walk(file_path):
            for filename in file_names:
                file_path = os.path.join(folder_name, filename)
                zip_object.write(file_path, os.path.basename(file_path))



def windows_compress():
    pass



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