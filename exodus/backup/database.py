import subprocess

def backup_database(config):
    db_type = config['database']['type']
    
    if db_type == 'mysql':
        backup_mysql_database(config['database'])
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
    
def backup_mssql_database(db_config):
    # Implement MySQL backup logic using subprocess to run MSSQLSERVER
    pass