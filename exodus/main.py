import argparse
from exodus.config.config_loader import ConfigLoader
from exodus.cloud.aws import upload_to_s3, create_s3_bucket
from exodus.backup.files import backup_files

def main():
    parser = argparse.ArgumentParser(description="Secure application transsfer tool")
    parser.add_argument('--config', required=True, help="Path to the configuration file")
    
    
    #Parsing the argument
    args = parser.parse_args()

    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    # Example: Backup files
    backup_dir = "/tmp/backup"
    backup_files(config['backup']['files'], backup_dir)

    # Example: Upload to S3
    bucket_name = config['cloud']['s3_bucket_name']
    create_s3_bucket(bucket_name)
    for file in config['backup']['files']:
        upload_to_s3(bucket_name, file)

if __name__ == "__main__":
    main()