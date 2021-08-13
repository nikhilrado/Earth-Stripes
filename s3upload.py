from s3keys import access_key, secret_access_key
import boto3
import os

client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

print(os.listdir())
upload_bucket = "ortana-test"
upload_file_path = 'test/test7b.png'
client.upload_file("test7.png", upload_bucket, upload_file_path,ExtraArgs={'ACL':'public-read', "ContentType":'image/png'})