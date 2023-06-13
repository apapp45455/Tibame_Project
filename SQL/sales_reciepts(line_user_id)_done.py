import pandas as pd
import pymysql
conn = pymysql.connect(host='host',
                                user='user',
                                password='password',
                                db='db')
cursor=conn.cursor()

sql = 'desc sales_reciepts'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])

user_id = input()

sql = f"""select * from sales_reciepts where customer_id='{user_id}' 
order by transaction_date desc, transaction_time desc 
limit 10;"""
cursor.execute(sql)
data = cursor.fetchall()
print(data)
df = pd.DataFrame(data, columns=columns)
print(df.to_string(index=False))
