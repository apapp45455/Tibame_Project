關於Google cloud platform上 Vertex AI API的說明文件
============================================================

本資料夾內包含:
1. 轉換成可被vertex AI辨識的[模型資料夾](#模型資料夾)
2. 從[Cloud SQL](#Cloud SQL)抓取特定資料
3. [自動部署模型到端點上，預測完畢後再取消部署模型](#自動部署與取消部署) 
4. 服務帳戶的JSON檔案 (**請注意!! 不要外流**)
5. GCP上定時執行，[設定VM](#VM相關設定)

## 模型資料夾
這裡將介紹如何將模型上傳至GCP上，有關模型轉換請參考[Model_Training](../Model_Training)

1. 將模型的資料夾上傳至cloud storage上
2. 啟用Vertex API，找到 Model Registry，點選匯入
3. 輸入模型名稱，點選繼續
4. 設定模型架構(若訓練模型時是使用tensorflow，即選擇tensorflow)，選擇訓練時的模型架構版本
5. 選擇模型的路徑(在cloud storage上的路徑)
6. 設定完成後點選左側的匯入

## Cloud SQL
總共分為三個程式，[sql_biscotti](./sql_biscotti.py)、[sql_pastry](./sql_pastry.py)、[sql_scone](./sql_scone.py)

1. 以apapp45455這個帳號連進去，
2. 在cloud SQL得到三個不同種類的每日銷售量並儲存成三個csv檔案
3. 再上傳到cloud storage內

詳情請看程式碼

## 自動部署與取消部署
總共分為三個程式，[vertex_Biscotti](./vertex_Biscotti.py)、[vertex_Pastry](./vertex_Pastry.py)、[vertex_Scone](./vertex_Scone.py)

1. 自動將模型部署到指定端點上
2. 從本地端讀入資料(資料從上面SQL指令產生)
3. 預測往後7天的銷售量，並分別儲存成不同.json
4. 上傳至cloud storage
5. 再從端點移除模型
6. 將預測結果化成折線圖，並且上傳到cloud storage上

詳情請見程式碼

## VM相關設定
gcp上虛擬機的名稱為vertexvm

開啟虛擬機的步驟:
1. 至compute engine，點選建立執行個體
2. 設定好名稱、地區、機器類型，直接按建立
3. 建立好後點選SSH，連線至虛擬機內
4. 點選上傳檔案，將上面的python程式、json、requirements.txt檔案上傳到虛擬機內
5. 若虛擬機內無安裝pip，執行sudo apt update，再執行sudo apt install python3-pip
6. 安裝環境 pip install -r requirements.txt
7. 輸入 chmod +x *.py，將python程式設為可執行
8. 設定工作排程，輸入crontab -e，輸入 i ，到最後一行輸入以下指令
    - 0 14 * * * /usr/bin/python3 /home/coffee_cloud01/sql_pastry.py >> /home/coffee_cloud01/sql.log 2>&1
    - 0 14 * * * /usr/bin/python3 /home/coffee_cloud01/sql_biscotti.py >> /home/coffee_cloud01/sql.log 2>&1 
    - 0 14 * * * /usr/bin/python3 /home/coffee_cloud01/sql_scone.py >> /home/coffee_cloud01/sql.log 2>&1
    - 0 15 * * * /usr/bin/python3 /home/coffee_cloud01/vertex_Biscotti.py >> /home/coffee_cloud01/Biscotti.log 2>&1
    - 0 15 * * * /usr/bin/python3 /home/coffee_cloud01/vertex_Pastry.py >> /home/coffee_cloud01/Pastry.log 2>&1
    - 0 15 * * * /usr/bin/python3 /home/coffee_cloud01/vertex_Scone.py >> /home/coffee_cloud01/Scone.log 2>&1
    - 表示在美國時間14時(台灣時間10點)，將執行sql.py檔案，隔一個小時執行vertex.py檔案
9. 使用crontab -l，查看是否已經有排程


