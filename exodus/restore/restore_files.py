import zipfile
import os

def unzip_file(zip_path, target_dir):
    """
    Unzips a file to the target directory.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"Unzipped {zip_path} to {target_dir}")
    except Exception as e:
        raise RuntimeError(f"Failed to unzip file: {e}")
