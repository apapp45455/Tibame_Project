# 說明: 這是一個酥皮的程式
# 先連結到cloud sql，並且將酥皮類的資料取出，並按照日期group by
# 整理好後分別存到兩個list中，再寫入sales.csv檔
# 然後將sales.csv檔上傳到cloud storage上

import configparser
import pymysql.cursors

config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')

host=config.get('host')
user=config.get('user')
password=config.get('password')
database=config.get('database')
bucket=config.get('bucket')

# Connect to the database
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database)

with connection:
    with connection.cursor() as cursor:
        sql = """SELECT transaction_date,sum(quantity) FROM coffee.sales_reciepts
               where product_id in (70, 72, 77, 78, 79)
               group by transaction_date;"""
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        
ls = list(result)

sales_dates = []
for date in ls:
   sales_dates.append((date[0].strftime("%Y/%m/%d")))

# print(sales_dates)
# ['2019/04/01', '2019/04/02', '2019/04/03', '2019/04/04', '2019/04/05', '2019/04/06', '2019/04/07', '2019/04/08', '2019/04/09', '2019/04/10', '2019/04/11', '2019/04/12', '2019/04/13', '2019/04/14', '2019/04/15', '2019/04/16', '2019/04/17', '2019/04/18', '2019/04/19', '2019/04/20', '2019/04/21', '2019/04/22', '2019/04/23', '2019/04/24', '2019/04/25', '2019/04/26', '2019/04/27', '2019/04/28', '2019/04/29', '2019/04/30', '2019/05/01', '2019/05/02', '2019/05/03', '2019/05/04', '2019/05/05', '2019/05/06', '2019/05/07', '2019/05/08', '2019/05/09', '2019/05/10', '2019/05/11', '2019/05/12', '2019/05/13', '2019/05/14', '2019/05/15', '2019/05/16', '2019/05/17', '2019/05/18', '2019/05/19', '2019/05/20', '2019/05/21', '2019/05/22', '2019/05/23', '2019/05/24', '2019/05/25', '2019/05/26', '2019/05/27', '2019/05/28', '2019/05/29', '2019/05/30', '2019/05/31']

sales_quantity = []
for quantity in ls:
   sales_quantity.append((int(quantity[1])))

# print(sales_quantity)
# [48, 32, 43, 49, 46, 35, 18, 23, 13, 36, 37, 47, 41, 16, 16, 14, 16, 17, 14, 13, 19, 13, 9, 15, 20, 17, 10, 21, 33, 18, 19, 16, 24, 28, 37, 39, 48, 44, 56, 51, 79, 92, 12, 29, 26, 23, 22, 37, 80, 67, 14, 21, 23, 76, 42, 60, 37, 17, 22, 22, 39]

import csv

# 開啟一個新的CSV文件並寫入資料
with open('Scone_sales.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(["date", "quantity"])  # 寫入
    # 繼續寫入資料
    for date, quantity in zip(sales_dates, sales_quantity):
        writer.writerow([date, quantity])


from google.cloud import storage

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
upload_blob(bucket, 'Scone_sales.csv', 'Scone_sales.csv')

