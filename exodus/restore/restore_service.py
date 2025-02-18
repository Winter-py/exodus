from flask import Flask, jsonify, request
import os
import zipfile
import boto3
from subprocess import run



app = Flask(__name__)

@app.route('/restore', methods=['POST'])
def restore():
    """
    Endpoint to handle restoration requests.
    Expects a JSON payload with S3 bucket, file key, and restore paths.
    """
    data = request.json
    s3_bucket = data.get('s3_bucket')
    s3_key = data.get('s3_key')
    restore_path = data.get('restore_path')
    database_details = data.get('database')

    if not all([s3_bucket, s3_key, restore_path]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Step 1: Download the ZIP file from S3
        zip_file_path = os.path.join('/tmp', os.path.basename(s3_key))
        s3_client = boto3.client('s3')
        s3_client.download_file(s3_bucket, s3_key, zip_file_path)
        print(f"Downloaded {s3_key} to {zip_file_path}")

        # Step 2: Unzip the files
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(restore_path)
        print(f"Extracted {zip_file_path} to {restore_path}")

        # Step 3: Restore the database (if provided)
        if database_details:
            db_type = database_details.get('type')
            db_host = database_details.get('host')
            db_user = database_details.get('user')
            db_password = database_details.get('password')
            db_name = database_details.get('name')
            db_dump_file = os.path.join(restore_path, database_details.get('dump_file'))

            if db_type == 'mysql':
                restore_command = [
                    'mysql',
                    f'-h{db_host}', f'-u{db_user}', f'-p{db_password}', db_name
                ]
                with open(db_dump_file, 'rb') as dump_file:
                    run(restore_command, stdin=dump_file)
                print(f"Restored MySQL database from {db_dump_file}")

        return jsonify({"status": "success", "message": "Restore completed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
    
    
def flask_app(host: str = "0.0.0.0", port: int = 5000):
    app.run(host=host, port=port)