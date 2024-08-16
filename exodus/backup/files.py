# backup_cli/backup/files.py

import os
import shutil

def backup_files(file_paths, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            shutil.copy(file_path, backup_dir)
        else:
            print(f"File {file_path} not found.")



def compress_files():
    pass