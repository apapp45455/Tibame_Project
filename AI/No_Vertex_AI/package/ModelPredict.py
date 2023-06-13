from sklearn.preprocessing import MinMaxScaler
import csv
import tensorflow as tf
import numpy as np

def Prediction(file_name: csv, model_name: str, timestep: int) -> list:
    # 讀取資料
    row_data = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            row_data.append(row)

    data = []
    for i in row_data:
        data.append(int(i[1]))

    # 正規化
    data = np.array(data)
    data = data.reshape(len(data),1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(data)
    ModelNew = tf.keras.models.load_model(model_name)

    dataNew = []
    for i in range(len(data)-timestep):
        dataNew.append(data[i:(i+timestep),0])
    dataNew = np.array(dataNew)

    for i in range(0, 7, 1):
        out = ModelNew.predict(dataNew)
        data = np.concatenate((data, out))

    output = scaler.inverse_transform(data)
    output = np.round(output[-7:])
    lst = output.tolist()
    new_lst = []
    for i in lst:
        new_lst.append(int(i[0]))

    return new_lst