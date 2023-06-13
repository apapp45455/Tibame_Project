import pandas as pd
import pymysql
conn = pymysql.connect(host='host',
                                user='user',
                                password='password',
                                db='db')
cursor=conn.cursor()

#取出欄位名稱
sql = 'desc sales_reciepts'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])

a = input('請輸入日期(YYYYMMDD)')
b = input('請輸入時間區間(7:00-19:59)')
b = b.split('-')

#利用輸入的日期及時間區間，查找符合的交易紀錄
sql = f"SELECT * FROM sales_reciepts where transaction_date={a} and transaction_time between '{b[0]}' and '{b[1]}'"
cursor.execute(sql)
data = cursor.fetchall()

df = pd.DataFrame(data, columns=columns)
print(df.to_string(index=False))

#有需要匯出csv檔案再執行以下指令
# Write data to CSV file
# csv_file = 'data.csv'
# df.to_csv(csv_file, index=False)
# return csv_file

cursor.close()
conn.close()
