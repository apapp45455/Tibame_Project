import pandas as pd
import pymysql
conn = pymysql.connect(host='host',
                                user='user',
                                password='password',
                                db='db')



cursor=conn.cursor()

#取出欄位名稱
sql = 'desc stock'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])


a = input('請輸入產品編號及進貨量(編號, 數量)')
a = list(map(int, a.split(',')))

#查找產品編號所代表之產品名稱及類別
sql = f'''select product_category, product_name from product where product_id={a[0]}'''
cursor.execute(sql)
b = cursor.fetchall()[0]

#利用查找到的產品名稱及類別搜尋庫存表中的該產品
sql = f"""select * from stock where product_category='{b[0]}' and product_name='{b[1]}'"""
cursor.execute(sql)
c = pd.DataFrame(cursor.fetchall(),columns=columns)

#修改產品數量及查找修改後的數據
sql = f"""update stock 
set total_quantity=total_quantity+{a[1]} 
where product_category='{b[0]}' 
and product_name='{b[1]}'"""
cursor.execute(sql)
conn.commit()
sql = f"""select * from stock where product_category='{b[0]}' and product_name='{b[1]}'"""
cursor.execute(sql)
d = pd.DataFrame(cursor.fetchall(),columns=columns)

print('原本庫存\n',c.to_string(index=False),'\n修改後庫存\n',d.to_string(index=False))
cursor.close()
conn.close()
