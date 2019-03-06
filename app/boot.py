import boto3
s3_client = boto3.client('s3')
s3_client.download_file('alpha-app-metadata-vis', 'app.db', 'app.db')