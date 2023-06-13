這台虛擬機不需要使用vertex ai，直接在vm裡面進行預測
三個程式碼分別是不同產品類別，其內容只有product kind(也就是產品種類)有所差異

程式碼執行說明:
1. 程式會呼叫cloud SQL，抓取最新版的資料，並儲存成csv檔，再將第二欄資料取出，進行正規化
2. 依照模型需要的輸入進行數據轉換
3. 將預測結果與日期打包成json格式，並上傳到cloud storage內

關於gcp schedule的設定:
==========================================================
1. 有兩個schedule，一個是開機，一個是關機
2. 現在的服務帳號為schedule開頭的，設定時需要給予**服務帳戶憑證建立者**、**Cloud Functions 叫用者**
3. 設定scheduler時**驗證標頭**選擇OIDC，再選擇所創設的服務帳號
4. 觸發一個新的function，就要開另一個schedule

關於gcp functions的設定:
==========================================================
1. 開機程式碼
```python
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def start_compute_engine(request):
    project = project
    zone = "us-central1-c"
    instance = instance_name

    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    request = service.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()

    return str(response)
```

2. 關機程式碼
```python
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def stop_compute_engine(request):
    project = project
    zone = "us-central1-c"
    instance = instance_name

    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('compute', 'v1', credentials=credentials)

    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()

    return str(response)
```

3. 其他注意事項

在gcp上的**進入點**框框內輸入的是你的function name，如start_compute_engine

要勾選使用https
