
import boto3
s3 = boto3.resource(service_name = 's3')
s3.meta.client.upload_file(Filename = 'app/app.db', Bucket = 'alpha-app-metadata-vis', Key = 'app.db')
