import json
import pandas as pd
import matplotlib.pyplot as plt

# 讀取 JSON 數據
with open('./Scone_data.json', 'r') as f:
    data = json.load(f)

# 檢查數據是否為字典
if type(data) is str:
    # 如果數據是字符串，再次使用 json.loads 轉換為字典
    data = json.loads(data)

# 將數據轉換為 pandas DataFrame
df = pd.DataFrame(list(data.items()), columns=['Date', 'Value'])

# 將日期轉換為 datetime 對象以便 matplotlib 能夠理解
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
