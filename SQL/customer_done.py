import pandas as pd
import pymysql
conn = pymysql.connect(host='host',
                                user='user',
                                password='password',
                                db='db')
cursor=conn.cursor()


sql = 'desc customer'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])

a=input('請輸入四位數會員編號或email:')

if len(a) == 4 or a=='Ub7626e192b3edeb51c2560dd43bb2a82':
    sql = f'select * from customer where customer_id="{a}"'
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data,columns=columns)
    print(df.to_string(index=False))
else:
    sql = f'''select * from customer where customer_email='{a}';'''
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data,columns=columns)
    print(df.to_string(index=False))

cursor.close()
conn.close()
