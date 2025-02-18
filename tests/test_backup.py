import requests
import argparse
from exodus.config.config_loader import ConfigLoader


def notify_machine_b(target_url, s3_bucket, s3_key, restore_path, database_details=None):
    """
    Notify Machine B to start the restore process.
    :param target_url: URL of Machine B's REST API
    :param s3_bucket: S3 bucket name
    :param s3_key: S3 object key
    :param restore_path: Path to restore the files
    :param database_details: Database details (optional)
    """
    payload = {
        "s3_bucket": s3_bucket,
        "s3_key": s3_key,
        "restore_path": restore_path,
        "database": database_details
    }
  
    try:
        response = requests.post(target_url, json=payload)
        response.raise_for_status()
        print(f"Machine B responded: {response.json()}")
    except requests.RequestException as e:
        print(f"Failed to notify Machine B: {e}")

#Load configuration from file
config_loader = ConfigLoader()
config = config_loader.load_config()

notify_machine_b(
    target_url="http://<machine-b-ip>:5000/restore",
    s3_bucket=config['cloud']['storage'],
    s3_key=config['backup']['files'],
    restore_path=config['restore']['path'],
    database_details=config['database']
)

