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
    cursor.close()
    conn.close()
    return data[0][0]

def updatestock():
    conn = pymysql.connect(host='34.81.244.137',
                                user='root',
                                password='tibame01',
                                db='coffee',
                                charset = 'utf8mb4')

    cursor = conn.cursor()
    sql = '''select * from sales_reciepts where sales_id=(select max(sales_id) from sales_reciepts)'''
    cursor.execute(sql)
    prod_id = cursor.fetchone()
    sql = f'''select * from product where product_id={prod_id[4]}'''
    cursor.execute(sql)
    prod_updating = cursor.fetchone()
    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[4]} 
    where product_category=(select product_category from product where product_id={prod_id[4]})
    and product_name=(select product_name from product where product_id={prod_id[4]});
    '''
    cursor.execute(sql)
    conn.commit()

    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[5]} 
    where product_category='milk'
    '''
    cursor.execute(sql)
    conn.commit()

    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[6]} 
    where product_name='package'
    '''
    cursor.execute(sql)
    conn.commit()

    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[7]} 
    where product_name='cup_sm'
    '''
    cursor.execute(sql)
    conn.commit()

    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[8]} 
    where product_name='cup_rg'
    '''
    cursor.execute(sql)
    conn.commit()

    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[9]} 
    where product_name='cup_lg'
    '''
    cursor.execute(sql)
    conn.commit()

    sql=f'''update stock 
    set total_quantity=total_quantity-{prod_id[5]}*{prod_updating[10]} 
    where product_name='box'
    '''
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()