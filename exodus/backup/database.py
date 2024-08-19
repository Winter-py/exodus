import subprocess
import tempfile
from files import store_backup_in_temp_dir


def backup_database(config):
    db_type = config['database']['type']
    
    if db_type == 'mysql':
        backup_mysql_database(config['database']['host'],config['database']['user'],config['database']['password'],config['database']['name'])
    # Add support for more databases here
    
    if db_type == 'mssql':
        backup_mssql_database(config['database'])


def backup_mysql_database(host,user,password,database,backup_file):
    # Construct the mysqldump command
    command = f"mysqldump -h {host} -u {user} -p{password} {database}"

    # Open the backup file and redirect the command output to it
    with open(backup_file, 'w') as output_file:
        subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.PIPE, universal_newlines=True)

    print(f"Backup completed and saved to {backup_file}.")
    
def backup_mssql_database(host,user,password,database,backup_file):
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
        print(f"Backup completed successfully and saved to {backup_path}.")
    else:
        print(f"Backup failed. Error: {result.stderr}")