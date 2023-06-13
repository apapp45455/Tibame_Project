import pymysql
import pandas as pd
import json

def salesreciepts(date, starttime, endtime):
    conn = pymysql.connect(
        host='34.81.244.137',
        user='root',
        password='tibame01',
        db='coffee')
    cursor=conn.cursor()
    sql = 'desc sales_reciepts'
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = []
    for i in range(len(data)):
        columns.append(data[i][0])

    sql = f"SELECT * FROM sales_reciepts where transaction_date='{date}' and transaction_time between '{starttime}' and '{endtime}';"
    cursor.execute(sql)
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)
    print(df.to_string(index=False))
    cursor.close()
    conn.close()
    return df.to_dict('list')

def salesreciepts_template(date, starttime, endtime):
    dataset = salesreciepts(date, starttime, endtime)
    message = {
        "type": "flex",
        "altText":'this is a flex message',
        "contents":{
            "type": "carousel",
            "contents": []
            }
    }
    for i in range(12):
        message_iter = {
            "type": "bubble",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "RECEIPT",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "銷售紀錄" + str(i),
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True
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
                                "text": "Transaction Date",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                              "type": "text",
                              "text": str(dataset['transaction_date'][i]),
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
                                "text": "Transaction Time",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(dataset['transaction_time'][i]),
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
                                "text": "Costomer ID",
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
                                "text": "Product ID",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['product_id'][i]),
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
                                "text": "Quantity",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['quantity'][i]),
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
                                "text": "Unit Price",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['unit_price'][i]),
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
                                "text": "Total Price",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['total_price'][i]),
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
                                "text": "Satisfication",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['satisfication'][i]),
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
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                          "type": "text",
                          "text": "PAYMENT ID",
                          "size": "xs",
                          "color": "#aaaaaa",
                          "flex": 0
                        },
                        {
                          "type": "text",
                          "text": "#743289384279",
                          "color": "#aaaaaa",
                          "size": "xs",
                          "align": "end"
                        }
                    ]
                }
              ]
            },
            "styles": {
                "footer": {
                    "separator": True
                }
            }
          }
        message['contents']['contents'].append(message_iter)
    return message

# 顧客端查詢
def client_salesreciepts(user_id):
    conn = pymysql.connect(
        host='34.81.244.137',
        user='root',
        password='tibame01',
        db='coffee')
    cursor=conn.cursor()
    sql = 'desc sales_reciepts'
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = []
    for i in range(len(data)):
        columns.append(data[i][0])

    sql = f"""select * from sales_reciepts where customer_id='{user_id}' 
            order by transaction_date desc, transaction_time desc 
            limit 10;"""
    cursor.execute(sql)
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)
    # print(df.to_string(index=False))
    cursor.close()
    conn.close()
    return df.to_dict('list')

def client_salesreciepts_template(user_id):
    dataset = client_salesreciepts(user_id)
    message = {
        "type": "flex",
        "altText":'this is a flex message',
        "contents":{
            "type": "carousel",
            "contents": []
            }
    }
    for i in range(10):
        message_iter = {
            "type": "bubble",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "RECEIPT",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "銷售紀錄" + str(i+1),
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True
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
                                "text": "Transaction Date",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                              "type": "text",
                              "text": str(dataset['transaction_date'][i]),
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
                                "text": "Transaction Time",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(dataset['transaction_time'][i]),
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
                                "text": "Product ID",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['product_id'][i]),
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
                                "text": "Quantity",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['quantity'][i]),
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
                                "text": "Unit Price",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['unit_price'][i]),
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
                                "text": "Total Price",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['total_price'][i]),
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
                                "text": "Satisfication",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(dataset['satisfication'][i]),
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
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                          "type": "text",
                          "text": "PAYMENT ID",
                          "size": "xs",
                          "color": "#aaaaaa",
                          "flex": 0
                        },
                        {
                          "type": "text",
                          "text": "#743289384279",
                          "color": "#aaaaaa",
                          "size": "xs",
                          "align": "end"
                        }
                    ]
                }
              ]
            },
            "styles": {
                "footer": {
                    "separator": True
                }
            }
          }
        message['contents']['contents'].append(message_iter)
    return message