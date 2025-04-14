import json
import os

import pandas as pd
from dotenv import load_dotenv
from result import attribution

from output import S3Uploader, TelegramSender

load_dotenv()

df = attribution('tables')
df.to_csv("output/attribution_results.csv", index=False)

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
json_path = os.path.join(parent_dir, 'config.json')

try:
    with open(json_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
except FileNotFoundError:
    print(f"Файл {json_path} не найден!")
except json.JSONDecodeError:
    print("Ошибка: файл не является валидным JSON!")


if config['service'] == 'Telegram':
    TOKEN = os.getenv('BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    tg = TelegramSender(TOKEN, CHAT_ID)
    tg.send_dataframe(df, 'attribution_results', config['output_file_format'])
    
if config['service'] == 'S3':
    S3_ACCESS_KEY= os.getenv('ACCESS_KEY'),
    S3_SECRET_KEY= os.getenv('SECRET_KEY'),
    S3_BUCKET_NAME= os.getenv('BUCKET_NAME')
    
    s3 = S3Uploader(S3_ACCESS_KEY, S3_SECRET_KEY)
    s3.upload_dataframe(S3_BUCKET_NAME)

