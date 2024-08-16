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

# backup_cli/backup/database.py

def backup_database(config):
    db_type = config['database']['type']
    
    if db_type == 'mysql':
        backup_mysql_database(config['database'])
    # Add support for more databases here
    
    if db_type == 'mssql':
        backup_mssql_database(config['database'])


def backup_mysql_database(db_config):
    # Implement MySQL backup logic using subprocess to run mysqldump
    pass

def backup_mssql_database(db_config):
    # Implement MySQL backup logic using subprocess to run MSSQLSERVER
    pass