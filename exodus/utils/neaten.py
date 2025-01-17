import os
import shutil
import tempfile

def clean_up_failed_backup():
    temp_dir = tempfile.gettempdir()
    backup_dir = os.path.join(temp_dir, 'backup')
    
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
        print(f"Cleaned up failed backup files in {backup_dir}")
    else:
        print(f"No backup files found in {backup_dir}")

def clean_up_successful_backup():
    temp_dir = tempfile.gettempdir()
    backup_dir = os.path.join(temp_dir, 'backup')
    
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
        print(f"Cleaned up successful backup files in {backup_dir}")
    else:
        print(f"No backup files found in {backup_dir}")