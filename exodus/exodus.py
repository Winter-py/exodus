import argparse
import tempfile
from exodus.config.config_loader import ConfigLoader
from exodus.cloud.aws import upload_to_s3, create_s3_bucket
from exodus.backup.files import backup_files
from exodus.backup.database import backup_database 

def main():
    #Initialize
    parser = argparse.ArgumentParser(description="Secure application transfer tool")
    parser.add_argument('-exce', '--config', help="Automate the transfer using a config file")
    parser.add_argument('-db', '--Database', help="Back up database", type=str) 
    
    
    #Parsing the argument
    args = parser.parse_args()


    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    #Backup files
    backup_dir = tempfile.gettempdir()
    backup_files(config['backup']['files'], backup_dir)

    #Backup Database
    backup_database(config['database']['type'],config)

    #Upload to S3
    region = config['cloud']['region']
    bucket_name = config['cloud']['s3_bucket_name']
    create_s3_bucket(region,bucket_name)
    for file in config['backup']['files']:
        upload_to_s3(bucket_name, file)


    if args.Database:
        print("something happned") 
    
    
if __name__ == "__main__":
    main()