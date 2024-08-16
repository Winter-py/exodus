import argparse
from exodus.config.config_loader import ConfigLoader
from exodus.cloud.aws import upload_to_s3, create_s3_bucket
from exodus.backup.files import backup_files

def main():
    #Initialize
    parser = argparse.ArgumentParser(description="Secure application transfer tool")
    parser.add_argument('-exce', '--config', help="Path to the configuration file")
    parser.add_argument('-db', '--Database', help="Back up database", type=str) 
    
    
    #Parsing the argument
    args = parser.parse_args()


    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    # Example: Backup files
    backup_dir = "/tmp/backup"
    backup_files(config['backup']['files'], backup_dir)

    # Example: Upload to S3
    region = config['cloud']['region']
    bucket_name = config['cloud']['s3_bucket_name']
    create_s3_bucket(region,bucket_name)
    for file in config['region']['backup']['files']:
        upload_to_s3(region,bucket_name, file)


    if args.Database:
        print("something happned") 
    
    
if __name__ == "__main__":
    main()