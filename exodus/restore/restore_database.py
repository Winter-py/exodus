from subprocess import run

def restore_mysql(database_details, dump_file_path):
    """
    Restore a MySQL database from a dump file.
    """
    db_host = database_details['host']
    db_user = database_details['user']
    db_password = database_details['password']
    db_name = database_details['name']

    try:
        restore_command = [
            'mysql', f'-h{db_host}', f'-u{db_user}', f'-p{db_password}', db_name
        ]
        with open(dump_file_path, 'rb') as dump_file:
            run(restore_command, stdin=dump_file, check=True)
        print(f"Restored MySQL database from {dump_file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to restore MySQL database: {e}")

def restore_database(database_type, database_details, dump_file_path):
    """
    Restore the database based on its type.
    """
    if database_type == 'mysql':
        restore_mysql(database_details, dump_file_path)
    else:
        raise ValueError(f"Unsupported database type: {database_type}")
