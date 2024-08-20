import subprocess
import tempfile 
 

def backup_database(db_type,config):
    # db_type = config['database']['type']
    
    if db_type == 'mysql':
        backup_mysql_database(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['name'],"test.sql")
    # Add support for more databases here
    
    if db_type == 'mssql':
        backup_mssql_database(config['database'])


def backup_mysql_database(host,user,password,database,backup_file):
    
    """
    Backs up a MySQL database to a specified file and moves the backup to the system's temporary directory.

    Args:
        host (str): The database server hostname.
        user (str): The database user.
        password (str): The database user's password.
        database (str): The name of the database to back up.
        backup_file (str): The path to the initial backup file.
    
    Returns:
        str: The full path to the stored backup file in the temp directory.
    """
    
    # Construct the mysqldump command
    command = f"mysqldump -h {host} -u {user} -p{password} {database}"

    # Open the backup file and redirect the command output to it
    with open(backup_file, 'w') as output_file:
       result = subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode == 0:
        print(f"Backup completed and saved to {backup_file}.")
        # Move the backup file to the system's temporary directory
        temp_backup_path = store_backup_in_temp_dir(backup_file)
        return temp_backup_path
    else:
        print(f"Backup failed. Error: {result.stderr}")
        return None

    
def backup_mssql_database(host,user,password,database,backup_file):
    
    """
    Backs up a MSSQLSERVER database to a specified file and moves the backup to the system's temporary directory.

    Args:
        host (str): The database server hostname.
        user (str): The database user.
        password (str): The database user's password.
        database (str): The name of the database to back up.
        backup_file (str): The path to the initial backup file.
    
    Returns:
        str: The full path to the stored backup file in the temp directory.
    """
    
    tmp = tempfile.gettempdir()
    backup_path =  tmp + f"\\dbbackup\\{backup_file}"
    # Construct the SQL command to perform the backup
    sql_command = f"BACKUP DATABASE [{database}] TO DISK = N'{backup_path}' WITH NOFORMAT, NOINIT, NAME = N'{database}-Full Database Backup', SKIP, NOREWIND, NOUNLOAD, STATS = 10"

    # Construct the sqlcmd command to run the SQL command
    command = f"sqlcmd -S {host} -U {user} -P {password} -Q \"{sql_command}\""

    # Execute the command
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    # Check if there was an error
    if result.returncode == 0:
        print(f"Backup completed and saved to {backup_file}.")
        # Move the backup file to the system's temporary directory
        temp_backup_path = store_backup_in_temp_dir(backup_file)
        return temp_backup_path
    else:
        print(f"Backup failed. Error: {result.stderr}")
        return None