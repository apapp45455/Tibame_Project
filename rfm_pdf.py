import os
from google.cloud import storage
import pandas as pd
from fpdf import FPDF
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './AI/Vertex_AI/tibame.json'

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """上傳文件到指定的cloud storage bucket"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # 儲存的雲端檔案名稱
    blob = bucket.blob(destination_blob_name)
    
    # 讀取的本地檔案名稱
    blob.upload_from_filename(source_file_name)

    print(f"File '{source_file_name}' uploaded to '{destination_blob_name}'.")

def rfm_pdf(bucket_name, source_blob_name, destination_file_name,  pdf_file, destination_blob_name):
    download_blob(bucket_name, source_blob_name, destination_file_name)
    # 讀取 CSV 檔案
    data = pd.read_csv('rfm_segment.csv')

    # 選取需要保留的欄位
    selected_columns = ['customer_id', 'Segment']
    data = data[selected_columns]

    # 將 "Segment" 欄位改為 "Status"
    data = data.rename(columns={'Segment': 'Status'})

    # 設定 PDF 報表相關設定
    pdf = FPDF()
    pdf.set_font("Arial", size=12)

    # 添加新頁面
    pdf.add_page()

    # 添加標題行（包括改名後的欄位名稱）
    for column in data.columns:
        pdf.cell(40, 10, column, 1, 0, 'C')
    pdf.ln()

    # 添加資料行
    for index, row in data.iterrows():
        pdf.cell(40, 10, str(row['customer_id']), 1, 0, 'C')
        pdf.cell(40, 10, str(row['Status']), 1, 0, 'C')
        pdf.ln()

    # 輸出 PDF 檔案
    pdf.output(pdf_file)

    #上傳到cloud storage
    upload_blob(bucket_name, pdf_file, destination_blob_name)

def rfm_pdf_template(address):
    message = {
        "type": "flex",
        "altText":'this is a flex message',
        "contents":{
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "下載顧客分群資料",
                        "weight": "bold",
                        "size": "xl",
                        "style": "normal",
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "下載",
                            "uri": address,
                        }
                    }
                    ],
                    "flex": 0
                        }
                        }
                        ]
                    }
            }
    return message