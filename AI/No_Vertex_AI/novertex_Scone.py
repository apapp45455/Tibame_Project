from package.cloudSQL import CloudSQLGetSales
from package.createSalesCSV import CreateCSV
from package.GCPStorage import upload_blob
from package.ModelPredict import Prediction
import configparser

import json
import os
import datetime

config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')

host=config.get('host')
user=config.get('user')
password=config.get('password')
database=config.get('database')
p_id = (70, 72, 77, 78, 79)
product_kind='Scone'
pretrainedModel = f'./LSTM_V1_{product_kind}.h5'
file_path = f"{product_kind}_sales.csv"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GOOGLE_APPLICATION_CREDENTIALS'
project=config.get('project')
bucket_name=config.get('bucket_name')
blob_name=f'{product_kind}_sales.csv'

sql = CloudSQLGetSales(host, user, password, database, p_id)
CreateCSV(sql, file_path)
predict = Prediction(file_path, pretrainedModel, 4)

# 創建日期
start_date = datetime.date(2019, 6, 1)
end_date = datetime.date(2019, 6, 7)
date_list = []
delta = datetime.timedelta(days=1)
while start_date <= end_date:
    date_list.append(start_date.strftime("%Y-%m-%d"))
    start_date += delta

# 將日期與預測銷售量綁成一份json檔案，並儲存到bucket
result = dict(zip(date_list, predict))
outputJson = json.dumps(result)

with open(f'{product_kind}_data.json', 'w') as f:
    json.dump(outputJson, f)

upload_blob(bucket_name, f'{product_kind}_data.json', f'{product_kind}_data.json')
