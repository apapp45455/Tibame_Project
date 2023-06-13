import pandas as pd
import pymysql
from google.cloud import storage

conn = pymysql.connect(host='host',
                                user='user',
                                password='password',
                                db='db')

cursor = conn.cursor()

#建立等等用來分析RFM分數的recency,frequency,monetary表格
# sql = """create or replace view RFM (customer_id,recency,frequency,monetary)
# as
# select customer_id, datediff(curdate(),date(max(transaction_date))), count(*) ,sum(total_price)
# from sales_reciepts
# group by customer_id
# order by customer_id;"""
# cursor.execute(sql)
# conn.commit()

#建立等等用來分析RFM分數的csv檔案(包含recency,frequency,monetary)
sql = """select customer_id, datediff(curdate(),date(max(transaction_date))), count(*) ,sum(total_price)
from sales_reciepts
group by customer_id
order by customer_id;"""
cursor.execute(sql)
data = cursor.fetchall()
columns = ['customer_id', 'recency', 'frequency', 'monetary']
# print(pd.DataFrame(data,columns=columns))
data = pd.DataFrame(data,columns=columns)
data.to_csv(r'./rfm.csv', index=0,encoding='utf-8-sig')

# 讀取資料
data = pd.read_csv('rfm.csv')

# 將RFM值轉換為RFM分數
r_labels = range(4, 0, -1)
r_quartiles = pd.qcut(data['recency'], 4, labels=r_labels)
f_labels = range(1, 5)
f_quartiles = pd.qcut(data['frequency'], 4, labels=f_labels)
m_labels = range(1, 5)
m_quartiles = pd.qcut(data['monetary'], 4, labels=m_labels)
data = data.assign(R=r_quartiles.values, F=f_quartiles.values, M=m_quartiles.values)

# 計算RFM分數總和
data['RFM Score'] = data[['R', 'F', 'M']].sum(axis=1)

# 依據RFM分數總和進行分群
def segment(rfm_score):
    if rfm_score >= 10:
        return 'VIP'
    elif rfm_score >= 6:
        return 'normal'
    else:
        return 'leaving'
data['Segment'] = data['RFM Score'].apply(segment)

# 如需看到單一顧客的類別
# print(data[data['customer_id']==5001])
# 如需所有顧客之資料，則存成csv供店家下載
data.to_csv(r'./rfm_segment.csv',index=0,encoding='utf-8-sig')
