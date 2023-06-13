from google.cloud import storage
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
from sklearn.preprocessing import MinMaxScaler

import configparser
import numpy as np
import os
import csv
import datetime
import json

config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')

def deploy_model(
    project_id: str,
    endpoint_id: str,
    model_id: str,
    deployed_model_display_name: str,
    location: str,
):
    """部署模型到端點上"""
    client = aiplatform.gapic.EndpointServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )

    deployed_model = {
        "model": client.model_path(project_id, location, model_id),
        "display_name": deployed_model_display_name,
        "dedicated_resources": {
            "machine_spec": {
                "machine_type": "n1-highcpu-2",
            },
            "min_replica_count": 1,
            "max_replica_count": 1,
        },
    }

    response = client.deploy_model(
        endpoint=client.endpoint_path(project_id, location, endpoint_id),
        deployed_model=deployed_model,
        traffic_split={"0": 100},
    )

    print("Long running operation:", response.operation.name)
    result = response.result()
    print("result:", result)

service=os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GOOGLE_APPLICATION_CREDENTIALS'
storage_client = storage.Client()
project=config.get('project')
location=config.get('location')
model_id=config.get('model_id')
model_name=config.get('model_name')
bucket_name=config.get('bucket_name')
endpoint_id=config.get('endpoint_id')
blob_name='Scone_sales.csv'
filename=f'gs://{bucket_name}/{blob_name}'
client = aiplatform_v1.services.prediction_service.PredictionServiceClient()

# 讀取資料
row_data = []
with open('./Scone_sales.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        row_data.append(row)

data = []
for i in row_data:
    data.append(i[1])

# 正規化
data = np.array(data)
data = data.reshape(len(data),1)
scaler = MinMaxScaler(feature_range=(0, 1))
# 模型訓練時使用的時間步長為4，所以取最後四天的資料
instance = scaler.fit_transform(data)[-4:]

# 從本地端要預測，需要將instances移除
instance_json = [{"lstm_8_input":instance.tolist()}]
# print(instance)

# 在網路上測試可以使用:
# data = {'instances': [{'lstm_68_input': [[0.09638554216867472], [0.1566265060240964], [0.1566265060240964], [0.3614457831325301]]}]}

# 部署模型到端點上
deploy_model(project, endpoint_id, model_id, model_name, location)

# 從端點預測數值
def endpoint_predict(
    project: str, location: str, instances: list, endpoint: str
):
    """從端點去預測銷售量"""
    aiplatform.init(project=project, location=location)

    endpoint = aiplatform.Endpoint(endpoint)

    prediction = endpoint.predict(instances=instances)
    return prediction

prediction_forward = []
# 一次預測7天資料，使用API預測7次
for i in range(0, 7, 1):
    response = endpoint_predict(project=project, location=location, instances=instance_json, endpoint=endpoint_id)
    prediction_value = float(response.predictions[0][0])
    # print(prediction_value)
    # 0.387070596
    prediction_forward.append(prediction_value)
    # 將預測的資料放到原本的資料的最後4天之後，也就是5/27~5/31再加一天，
    # 再拿5/28~6/1的資料做一次預測，以此類推
    instance = np.append(instance, [[prediction_value]], axis=0)
    instance = instance[-4:]
    instance_json = [{"lstm_8_input":instance.tolist()}]
    print(i+1, "done")

# 反正規化
prediction_forward = np.array(prediction_forward).reshape(-1, 1)
output = scaler.inverse_transform(prediction_forward)
output = np.round(output)
lst = output.tolist()

inverse_instance = []
for i in lst:
    inverse_instance.append(int(i[0]))

start_date = datetime.date(2019, 6, 1)
end_date = datetime.date(2019, 6, 7)

date_list = []
delta = datetime.timedelta(days=1)
while start_date <= end_date:
    date_list.append(start_date.strftime("%Y-%m-%d"))
    start_date += delta

# 將日期與預測銷售量綁成一份json檔案，並儲存到bucket
result = dict(zip(date_list, inverse_instance))
outputJson = json.dumps(result)

with open('Scone_data.json', 'w') as f:
    json.dump(outputJson, f)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """上傳文件到指定的cloud storage bucket"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # 儲存的雲端檔案名稱
    blob = bucket.blob(destination_blob_name)
    
    # 讀取的本地檔案名稱
    blob.upload_from_filename(source_file_name)

    print(f"File '{source_file_name}' uploaded to '{destination_blob_name}'.")

# 呼叫上面函數，將sales.csv上傳到bucket
upload_blob('speech-ai101-bucket', 'Scone_data.json', 'Scone_prediction.json')

# 一切都完成後取消部署模型
def undeploy_model(
    project_id: str,
    endpoint_id: str,
    deployed_model_id: str,
    location: str,
):
    """取消部署模型"""
    client = aiplatform.gapic.EndpointServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )

    response = client.undeploy_model(
        endpoint=client.endpoint_path(project_id, location, endpoint_id),
        deployed_model_id=deployed_model_id,
        traffic_split={},
    )

    print("Long running operation:", response.operation.name)
    result = response.result()
    print("result:", result)

def get_deployed_model_id(project_id: str, endpoint_id: str, location: str = "us-central1"):
    """獲取部署到端點的模型ID"""
    client = aiplatform_v1.EndpointServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
    endpoint = client.get_endpoint(
        name=client.endpoint_path(project_id, location, endpoint_id)
    )

    deployed_model_id = endpoint.deployed_models[0].id

    return deployed_model_id

deployed_model_id = get_deployed_model_id(project, endpoint_id)

undeploy_model(project, endpoint_id, deployed_model_id, location)


import pandas as pd
import matplotlib.pyplot as plt

# 讀取 JSON 數據
with open('./Scone_data.json', 'r') as f:
    data = json.load(f)

# 檢查數據是否為字典
if type(data) is str:
    # 如果數據是字串，再次使用 json.loads 轉換為字典
    data = json.loads(data)

# 將數據轉換為 pandas DataFrame
df = pd.DataFrame(list(data.items()), columns=['Date', 'Value'])

# 將日期轉換為 datetime
df['Date'] = pd.to_datetime(df['Date'])

# 設置日期為索引
df.set_index('Date', inplace=True)

# 使用 matplotlib 繪製折線圖
plt.figure(figsize=(10, 6))
plt.plot(df['Value'], marker='o')
plt.title('Scone Prediction')
plt.xlabel('Date')
plt.ylabel('Quantity')
plt.grid(True)
for x, y in zip(df.index, df['Value']):
    plt.text(x, y, str(y))
plt.savefig('./Predict_Scone.png')

upload_blob('speech-ai101-bucket', 'Predict_Scone.png', 'Predict_Scone.png')