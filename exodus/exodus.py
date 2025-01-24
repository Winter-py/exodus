import argparse
import tempfile
from datetime import datetime
from exodus.config.config_loader import ConfigLoader
from exodus.cloud.aws import create_s3_bucket, upload_zip_to_s3
from exodus.backup.files import backup_files, zip_files_in_directory
from exodus.backup.database import backup_database 

def main():
    #Initialize
    parser = argparse.ArgumentParser(description="Secure application transfer tool. Use this tool to back up files, optionally back up a database, compress files, and upload them to a cloud storage provider.")
    parser.add_argument('-exce', '--config', help="Automate the transfer using a config file")
    parser.add_argument('-db', '--Database', help="Back up database", type=str)
    parser.add_argument('-r', '--Restore', help="Restore a backup")
    parser.add_argument('-A', '--auto', help="Automate transfer unpacking and restoration", action='store_true')
    
    
    #Parsing the argument
    args = parser.parse_args()


    # Handle missing config file
    if not args.config:
        print("No configuration file specified.")
        use_interactive = input("Do you want to enter configuration details interactively? (yes/no): ").strip().lower()
        if use_interactive == 'yes':
            cloud = input("Enter the cloud provider (aws): ").strip().lower()
            if cloud == 'aws':
                region = input("Enter the AWS region: ").strip()
                s3_bucket_name = input("Enter the S3 bucket name: ").strip()
                backup_files_path = input("Enter the path of files to back up: ").strip()
            
            # if cloud == 'Azure':
            #     region = input("Enter the Azure region: ").strip()
            #     azure_blob_storage = input("Enter the Azure storage account name: ").strip()
            #     backup_files_path = input("Enter the path of files to back up: ").strip()

            # Create a basic config dictionary
            config = {
                'cloud': {'region': region, 'storage': s3_bucket_name},
                'backup': {'files': backup_files_path},
                'database': {'type': args.Database or None}
            }
        else:
            print("Exiting... Please provide a configuration file using the --config argument.")
            return
    else:
        # Load configuration from file
        config_loader = ConfigLoader(args.config)
        config = config_loader.load_config()
    
    #datatime 
    # current dateTime
    now = datetime.now()
    # convert to string
    date_time_str = now.strftime("%Y%m%d%H%M%S")

    #Backup files
    backup_dir = tempfile.gettempdir() + f"\\E{date_time_str}"
    backup_files(config['backup']['files'], backup_dir)
    
    #Backup Database (Untested)
    # backup_database(config['database']['type'],config)
    
    # Compress files 
    zip_file_path = zip_files_in_directory(backup_dir)
    

    #Upload to S3
    region = config['cloud']['region']
    bucket_name = config['cloud']['s3_bucket_name']
    create_s3_bucket(region,bucket_name)
    upload_zip_to_s3(bucket_name, zip_file_path)

    if args.Database:
        print("something happned") 
    
    
if __name__ == "__main__":
    main()