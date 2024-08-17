import os
import shutil
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

