from google.cloud import storage
from google.oauth2 import service_account

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_path):
    """上傳檔案至 Google Cloud Storage (GCS)"""
    # 載入服務帳戶金鑰
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    # 建立 GCS 客戶端
    client = storage.Client(credentials=credentials)

    # 取得指定的 Bucket
    bucket = client.get_bucket(bucket_name)

    # 建立 Blob 物件，並指定上傳的檔案名稱
    blob = bucket.blob(destination_blob_name)

    # 上傳檔案到 GCS
    blob.upload_from_filename(source_file_path)

    print(f"已成功上傳檔案至 gs://{bucket_name}/{destination_blob_name}。")

# 設定 GCS Bucket 名稱、本地檔案路徑、目標 Blob 名稱和服務帳戶金鑰路徑
bucket_name = "bucket_name"
source_file_path = "source_file_path"
destination_blob_name = "destination_blob_name"
credentials_path = 'YOUR_CREDENTIALS_PATH'

# 執行上傳
upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_path)
