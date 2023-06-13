關於模型訓練與轉換
=========================================

### 概要:
1. [設定目標](#設定目標)
2. [資料來源](#資料來源)
3. [資料前處理](#資料前處理)
4. [訓練模型](#訓練模型)
5. 模型[預測與測量誤(mse)](#預測與測量誤差)
6. [儲存模型](#輸出模型)
7. [模型轉換](#模型轉換)

## 設定目標

本專案主要想解決小商家的備料問題，像是咖啡廳的糕點、麵包等等，當天無法賣出就必須銷毀，因此，我們使用深度學習來**預測未來的銷售量**。

## 資料來源

使用[kaggle](https://www.kaggle.com/datasets/ylchang/coffee-shop-sample-data-1113)上的資料庫，並利用此資料庫生成下個月的資料。

## 資料前處理

我們先來查看資料，跟銷售量有關的表格是"sraapril.csv"、"sramay.csv"，也就是兩個月份的銷售紀錄，之後我們分別做了以下處理:
1. 產品中有時效性的總共可分為三類，分別為Biscotti, Pastry, Scone
2. 依照產品編號，分成三種不同種類的jupyter notebook，[Biscotti](./GRU_V1_Biscotti.ipynb)、[Pastry](./GRU_V1_Pastry.ipynb)、[Scone](./GRU_V1_Scone.ipynb)
3. 挑選檔案中的交易日期"transaction_date"、產品編號"product_id"、數量"quantity"
4. 按照各類型產品的編號，將當天同種類的商品數量相加，並轉成DataFrame，index設為交易日期
5. 將四、五月的資料做合併，並將空值去除
6. 將資料以Minmaxscaler做正規化，將數值變成0~1之間的數值，以加速模型處理

## 訓練模型

我們使用RNN循環神經網路，其能夠處理具有時間序列的任務，像是天氣變化、網站造訪者數量等

1. 定義函數，分割data與label，data是輸入給模型的資料，模型將根據data預測label的資料，例如: data為4/1~4/4的資料，模型將預測4/5的資料，此時的label即4/5的資料
2. 我們將資料切割成訓練集與測試集，比例為7:3，時間步長設為4，也就是以前四天預測下一天數值
3. 使用函數，取得訓練集與測試集的data與label
4. RNN模型選用LSTM，其輸入的資料必須是三維資料，分別為batch_size, time_steps, input_dim，因此必須更改資料維度
5. 定義模型，嘗試更改模型層數、每層的神經元數量、dropout的比例，注意第一層必須給予**return_sequence=True**
6. 查看模型的input_names，作為往後vertex AI的輸入值
7. 建立模型與開始訓練模型，優化器選用Adam，損失函數為mean_squared_error，嘗試更改學習率、訓練次數、batch_size
8. 輸出每個周期的損失值，以確定模型確實在學習資訊

## 預測與測量誤差

1. 使用model.predict預測訓練集與測試集的資料
2. 將預測出來的資料反正規化，轉換成原始數值，並使用matplotlib繪圖，圖像化預測數值與真實數值的差異
3. 使用keras中的MeanSquaredError，輸出預測的誤差值

## 輸出模型

輸出誤差值最小的模型，做為最終版的模型

## 模型轉換

輸出的模型副檔名為.h5，使用hdf5_to_savemodel.py，將模型轉換成vertex ai可使用的格式

請在shell內輸入: python ./hdf5_to_savemodel.py ./欲轉換的模型

如果在虛擬機內運行，直接使用.h5檔案即可

## 模型誤差與參數

[Notion連結](https://boiling-babcat-6c1.notion.site/RNN-Models-d6025392639e4049996d1978cc83a838)
