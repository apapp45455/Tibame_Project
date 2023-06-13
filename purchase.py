import pymysql
import pandas as pd
import json

def purchased(prod_no, prod_quantity):
    conn = pymysql.connect(
        host='34.81.244.137',
        user='root',
        password='tibame01',
        db='coffee')
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
    sql = f"select product_category, product_name from product where product_id='{prod_no}'"; 
    cursor.execute(sql)
    prod_detail = cursor.fetchall()[0]

    #利用查找到的產品名稱及類別搜尋庫存表中的該產品
    sql = f"select * from stock where product_category='{prod_detail[0]}' and product_name='{prod_detail[1]}';"
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

    # print('原本庫存\n',prod_before.to_string(index=False),'\n修改後庫存\n',prod_after.to_string(index=False))
    cursor.close()

    prod_before_dict = prod_before.to_dict('list')
    prod_after_dict = prod_after.to_dict('list')
    conn.close()
    return prod_before, prod_after


def purchase_template(prod_no , prod_quantity):
    before_dataset, after_dataset = purchased(prod_no , prod_quantity)


    message = {
    "type":"flex",
    "altText": "this is a flex message",   
    "contents":{
        "type": "carousel",
        "contents": []
    }
}
    for i in range(1): 
        flex_content = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "purchase",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "庫存查詢",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "查詢庫存變化",
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
                                "text": "原庫存量",
                                "size": "lg",
                                "color": "#555555",
                                "flex": 0,
                                "decoration": "underline"
                            },
                            {
                                "type": "text",
                                "text": "stock_before",
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
                                "text": "product_category",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(before_dataset['product_category'][0]),
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
                                "text": "product_name",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(before_dataset['product_name'][0]),
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
                                "text": "purchase_price",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(before_dataset['purchase_price'][0]),
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
                                "text": "total_quantity",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(before_dataset['total_quantity'][0]),
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
                                "text": "quantity_warning",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(before_dataset['quantity_warning'][0]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
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
                            "margin": "xxl",
                            "contents": [
                            {
                                "type": "text",
                                "text": "現有庫存量",
                                "size": "lg",
                                "color": "#555555",
                                "decoration": "underline"
                            },
                            {
                                "type": "text",
                                "text": "stock_after",
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
                                "text": "product_category",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(after_dataset['product_category'][0]),
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
                                "text": "product_name",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(after_dataset['product_name'][0]),
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
                                "text": "purchase_price",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(after_dataset['purchase_price'][0]),
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
                                "text": "total_quantity",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(after_dataset['total_quantity'][0]),
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
                                "text": "quantity_warning",
                                "size": "sm",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(after_dataset['quantity_warning'][0]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
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
                            "contents": [
                            {
                                "type": "text",
                                "text": "CHANGE",
                                "size": "sm",
                                "color": "#555555"
                            },
                            {
                                "type": "text",
                                "text": str(after_dataset['total_quantity'][0] - before_dataset['total_quantity'][0]),
                                "size": "sm",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
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
              
        message["contents"]["contents"].append(flex_content)
        
    return message
