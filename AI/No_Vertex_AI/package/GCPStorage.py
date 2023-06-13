from google.cloud import storage

def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """上傳文件到指定的cloud storage bucket"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # 儲存的雲端檔案名稱
    blob = bucket.blob(destination_blob_name)
    
    # 讀取的本地檔案名稱
    blob.upload_from_filename(source_file_name)

    return f"File '{source_file_name}' uploaded to '{destination_blob_name}'."