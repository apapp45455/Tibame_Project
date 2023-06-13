from linebot.models import *
import pymysql
import pandas as pd
from tabulate import tabulate


def transaction_records(event):
    # 如果觸發postback.data == 'CALL_MYSQL'就會回傳一個TextSendMessage的物件
    if event.postback.data == 'CALL_MYSQL':
        try:
            # 連接資料庫
            connection = pymysql.connect(host='34.81.244.137',
                                        user='root',
                                        password='tibame01',
                                        db='coffee')
            if connection:
                print("資料庫已連線")
            connection.close()
            print("資料庫已關閉")
        except Exception as e:
            print("錯誤:", e)
            
            # # 執行 MySQL 查詢
            # with connection.cursor() as cursor:
            #     sql = """
            #         SELECT c.customer_id AS '客戶編號', c.transaction_date AS '交易日期', c.transaction_time AS '交易時間', 
            #         p.product_name AS '產品名稱', c.quantity AS '數量', c.total_price AS '總價'
            #         FROM cafetest1 c
            #         INNER JOIN product p ON c.product_id = p.product_id
            #         ORDER BY c.customer_id ASC, c.transaction_date DESC, c.transaction_time DESC
            #         """
            # cursor.execute(sql)
            # results = cursor.fetchall()

            # # 如果查詢結果為空，則回傳無消費紀錄訊息
            # if not results:
            #     return '目前無任何消費紀錄。'

            # # 將查詢結果轉換為 Pandas DataFrame，並篩選出指定欄位
            # df = pd.DataFrame(results, columns=['客戶編號', '交易日期', '交易時間', '產品名稱', '數量', '總價'])

            # # 轉換日期時間格式，以便顯示
            # df['交易日期'] = pd.to_datetime(df['交易日期'])
            # df['交易時間'] = pd.to_timedelta(df['交易時間']).dt.total_seconds().apply(lambda x: timedelta(seconds=x))
            # df['消費時間'] = df['交易日期'] + df['交易時間']
            # df['消費時間'] = df['消費時間'].dt.strftime('%Y-%m-%d %H:%M')
            # df = df[['客戶編號', '消費時間', '產品名稱', '數量', '總價']] # 移除交易日期和交易時間欄位

            # # 將 DataFrame 轉換為文字表格，以便顯示
            # table = tabulate(df, headers='keys', tablefmt='simple', showindex=False)

            # return TextSendMessage(text=f'這是所有客戶的歷史消費紀錄：\n\n{table}')
   