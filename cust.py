import pandas as pd
import pymysql
import json
from rfmtest import get_cust

def check_customer(customer_id):
    conn = pymysql.connect(
    host='34.81.244.137',
    user='root',
    password='tibame01',
    db='coffee'
    )
    cursor=conn.cursor()
    sql = "SELECT COUNT(*) FROM customer WHERE customer_id = %s"
    cursor.execute(sql, customer_id)
    result = cursor.fetchone()

    exists = result[0] > 0
    return exists

def customer(info):
    conn = pymysql.connect(
    host='34.81.244.137',
    user='root',
    password='tibame01',
    db='coffee'
    )
    cursor=conn.cursor()
    sql = 'desc customer'
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = [row[0] for row in data]

    if isinstance(info, list):
        # 判斷info是否為list型態
        id_list = ', '.join(['%s'] * len(info))
        sql = f'select * from customer where customer_id in ({id_list});'
        cursor.execute(sql, info)
    else:
        raise ValueError("Invalid data type. Only list data is accepted.")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    # print(df.to_string(index=False))
    cursor.close()
    conn.close()
    cust_dict = df.to_dict('list')
    return cust_dict

def customers(text):
    dataset = customer(text)
    bubbles = []
    
    for i in range(len(dataset['customer_id'])):
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "會員資料",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "customer_id",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(dataset['customer_id'][i]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "customer_email",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": dataset['customer_email'][i],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "customer_since",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": dataset['customer_since'][i].strftime('%Y-%m-%d'),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "birthdate",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": dataset['birthdate'][i].strftime('%Y-%m-%d'),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "gender",
                                    "size": "sm",
                                    "color": "#555555"
                                },
                                {
                                    "type": "text",
                                    "text": dataset['gender'][i],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "occupation",
                                    "size": "sm",
                                    "color": "#555555"
                                },
                                {
                                    "type": "text",
                                    "text": dataset['occupation'][i],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "hobby",
                                    "size": "sm",
                                    "color": "#555555"
                                },
                                {
                                    "type": "text",
                                    "text": dataset['hobby'][i],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "fav_drinks",
                                    "color": "#555555",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": dataset['fav_drinks'][i],
                                    "color": "#111111",
                                    "size": "sm",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "fav_foods",
                                    "color": "#555555",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": dataset['fav_foods'][i],
                                    "align": "end",
                                    "color": "#111111",
                                    "size": "sm"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "customer category",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": get_cust(dataset['customer_id'][i]),
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            }
                    ]
                },
                        {
                        "type": "separator",
                        "margin": "xxl"
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }   
                }
            }
        bubbles.append(bubble)
    message = {
        'type': 'flex',
        'altText': 'this is a flex message',
        'contents': {
            'type': 'carousel',
            'contents': bubbles
        }
    }
    return message