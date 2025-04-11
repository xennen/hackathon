import requests
import os
from io import StringIO, BytesIO
import boto3
from botocore.client import Config

class TelegramSender:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_dataframe(self, df, filename='data', format='csv'):
        if format == 'csv':
            file_data = df.to_csv(index=False)
            file_obj = StringIO(file_data)
            file_ext = 'csv'
            mime_type = 'text/csv'
        elif format == 'xlsx':
            file_obj = BytesIO()
            df.to_excel(file_obj, index=False)
            file_obj.seek(0)
            file_ext = 'xlsx'
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            raise ValueError("Поддерживаются только CSV и XLSX форматы")

        files = {
            'document': (f"{filename}.{file_ext}", file_obj, mime_type)
        }
        
        response = requests.post(
            f"{self.base_url}/sendDocument",
            data={'chat_id': self.chat_id},
            files=files
        )
        
        return response.json()
    
class S3Uploader:
    def __init__(self, access_key, secret_key):
        self.s3 = boto3.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4')
        )

    def upload_dataframe(self, df, bucket_name, s3_key="", format='csv'):
        path = f"/{s3_key.split('/')[-1]}"
        
        if format == 'csv':
            df.to_csv(path, index=False)
            content_type = 'text/csv'
        elif format == 'xlsx':
            df.to_excel(path, index=False)
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            raise ValueError("Поддерживаются только CSV и XLSX форматы")

        self.s3.upload_file(
            path,
            bucket_name,
            s3_key,
            ExtraArgs={'ContentType': content_type}
        )
        
        os.remove(path)
        return f"s3://{bucket_name}/{s3_key}"