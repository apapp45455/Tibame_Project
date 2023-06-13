import pandas as pd
import pymysql
conn = pymysql.connect(
    host='host',
    user='user',
    password='password',
    db='db'
    )
def customer(info):
    cursor=conn.cursor()
    sql = 'desc customer'
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = []
    for i in range(len(data)):
        columns.append(data[i][0])

    if len(info) == 4:
        a = int(info)
        sql = f'select * from customer where customer_id={a};'
        cursor.execute(sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data,columns=columns)
        print(df.to_string(index=False))
        cursor.close()
        return df.to_string(index=False)
    else:
        sql = f'select * from customer where customer_email={info};'
        cursor.execute(sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data,columns=columns)
        print(df.to_string(index=False))
        cursor.close()
        return df.to_string(index=False)
conn.close()

def salesreciepts(date, starttime, endtime):
    cursor=conn.cursor()
    sql = 'desc sales_reciepts'
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = []
    for i in range(len(data)):
        columns.append(data[i][0])

    sql = f"SELECT * FROM sales_reciepts where transaction_date={date} and transaction_time between {starttime} and {endtime};"
    cursor.execute(sql)
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)
    print(df.to_string(index=False))
    cursor.close()
    
    return df.to_string(index=False)
conn.close()

def purchase(prod_no, prod_quantity):
    cursor=conn.cursor()

    #取出欄位名稱
    sql = 'desc stock'
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = []
    for i in range(len(data)):
        columns.append(data[i][0])

    # a = input('請輸入產品編號及進貨量(編號, 數量)')
    # a = list(map(int, a.split(',')))

    #查找產品編號所代表之產品名稱及類別
    sql = f'''select product_category, product_name from product where product_id={prod_no}'''
    cursor.execute(sql)
    prod_detail = cursor.fetchall()[0]

    #利用查找到的產品名稱及類別搜尋庫存表中的該產品
    sql = f"""select * from stock where product_category='{prod_detail[0]}' and product_name='{prod_detail[1]}'"""
    cursor.execute(sql)
    prod_before = pd.DataFrame(cursor.fetchall(),columns=columns)

    #修改產品數量及查找修改後的數據
    sql = f"""update stock 
    set total_quantity=total_quantity+{prod_quantity} 
    where product_category='{prod_detail[0]}' 
    and product_name='{prod_detail[1]}'"""
    cursor.execute(sql)
    conn.commit()
    sql = f"""select * from stock where product_category='{prod_detail[0]}' and product_name='{prod_detail[1]}'"""
    cursor.execute(sql)
    prod_after = pd.DataFrame(cursor.fetchall(),columns=columns)

    print('原本庫存\n',prod_before.to_string(index=False),'\n修改後庫存\n',prod_after.to_string(index=False))
    cursor.close()
    return '原本庫存\n',prod_before.to_string(index=False),'\n修改後庫存\n',prod_after.to_string(index=False)
conn.close()
