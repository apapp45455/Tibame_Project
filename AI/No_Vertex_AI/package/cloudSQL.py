import pymysql.cursors

def CloudSQLGetSales(host: str, user: str, password: str, database: str, p_id: tuple) -> list:
    """連結到cloudSQL，取得產品種類的銷售數量"""
    # Connect to the database
    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                database=database)

    with connection:
        with connection.cursor() as cursor:
            sql = f"""SELECT transaction_date,sum(quantity) FROM coffee.sales_reciepts
                where product_id in {p_id}
                group by transaction_date;"""
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
        
    ls = list(result)
    
    return ls