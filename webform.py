import pymysql
from datetime import datetime
def writedata(data:list):

    conn = pymysql.connect(host='34.81.244.137',
                                user='root',
                                password='tibame01',
                                db='coffee',
                                charset = 'utf8mb4')

    cursor = conn.cursor()
    
    sql = f"""
    select product_id,sale_price from product where product_category='{data[1]}' and product_name='{data[2]}' and unit=1
    """
    cursor.execute(sql)
    product = cursor.fetchall()
    transaction_date = str(datetime.today().date()).replace('-','')
    transaction_time = str(datetime.today().time())[:8]
    sql = f"""
    insert into sales_reciepts(transaction_date, transaction_time, customer_id, product_id, quantity, unit_price, total_price)
    values('{transaction_date}','{transaction_time}','{data[0]}','{product[0][0]}','{data[3]}','{product[0][1]}','{int(data[3])*float(product[0][1])}')
    """

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def showtotal():

    conn = pymysql.connect(host='34.81.244.137',
                                user='root',
                                password='tibame01',
                                db='coffee',
                                charset = 'utf8mb4')

    cursor = conn.cursor()

    sql = """select total_price from sales_reciepts order by transaction_date desc, transaction_time desc limit 1"""
    cursor.execute(sql)
    data = cursor.fetchall()
    return data[0][0]