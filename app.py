from __future__ import unicode_literals
import string
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import requests
import re
import json
import configparser
import os
from urllib import parse
import string
import pymysql
import pandas as pd
import openpyxl
from datetime import datetime
from storemodule import *
from cust import *
from rfmtest import get_cust
from salesreciept import *
from purchase import *
from recommendation_guest import *
from search_product import *
from member_customer import member_template
from dashboard import dashboard
from member_store import memberdata
from rfm_pdf import *
from picker import *
import webform

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
line_login_id = config.get('line-bot', 'line_login_id')
line_login_secret = config.get('line-bot', 'line_login_secret')
my_phone = config.get('line-bot', 'my_phone')
google_map_key = config.get('line-bot', 'google_map_key')
google_map_url = config.get('line-bot', 'google_map_url')
id_file_name = './d_list.xlsx' # File name
sheet_name = 'worksheet1' # 4th sheet
sheet_header = 0 # The header is the 2nd row
bucket_name='speech-ai101-bucket'
source_file_name='rfm_segment.pdf'
destination_blob_name='rfm_segment.pdf'
destination_file_name="rfm_segment.csv"
source_blob_name="rfm_segment.csv"
pdf_file = 'rfm_segment.pdf'
file_ad = "https://storage.googleapis.com/speech-ai101-bucket/rfm_segment.pdf"

#http的HEADER
HEADER = {  
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}
state, date, stime, etime, customer_list = {}, None , None, None, []
@app.route("/", methods=['POST', 'GET'])
def index():
    # state = None
    global customer_list
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    if request.method == 'POST' and len(events) == 0:
        return 'ok'
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        userid = events[0]["source"]["userId"]
        payload["to"] = userid
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]
                if text == "尋找商品":
                    payload["messages"] = [product_template()]
                elif text == "價目表":
                    payload["messages"] = [product_type()]
                elif text == "咖啡豆":
                    payload["messages"] = [bean_menu()]
                elif text == "茶飲":
                    payload["messages"] = [tea_menu()]
                elif text == "咖啡":
                    payload["messages"] = [coffee_menu()]
                elif text == "甜品":
                    payload["messages"] = [bakery_menu()]
                elif text == "精選商品":
                    state[userid] = {"status": "awaiting_member_id"}                
                    customer_id = 'Ub7626e192b3edeb51c2560dd43bb2a82'
                    payload["messages"] = [recommend_template(customer_id)]
                    del state[userid]
                elif text == "店鋪資訊":
                    payload["messages"] = [store_information()]
                elif text == "附近景點":
                    payload["messages"] = [get_attractions()]
                elif text == "會員專區":
                    payload["messages"] = [member_template()]
                elif text == "消費記錄":
                    state[userid] = {"status": "awaiting_member_id"} 
                    customer_id = 'Ub7626e192b3edeb51c2560dd43bb2a82'
                    payload["messages"] = [client_salesreciepts_template(customer_id)]  
                    del state[userid]           
                elif text == "線上訂餐":
                    payload["messages"] = []
                elif text == "協助頁面":
                    payload["messages"] = [problem_information()]
                elif text == "訂單問題":
                    payload["messages"] = [order_problem_template()]
                elif text == "會員資訊":
                    payload["messages"] = [memberdata()]
                elif text == "查詢會員資訊":
                    state[userid] = {"status": "awaiting_member_id", "customer_list": []}
                    payload["messages"] = [{"type": "text", "text": "請輸入要查詢的會員編號 (ex.5001)，輸入 end 結束："}]
                elif state.get(userid) and state[userid]["status"] == "awaiting_member_id":
                    if text == "end":
                        customer_list = state[userid]["customer_list"]
                        if customer_list:
                            payload["messages"] = [customers(customer_list)]
                        else:
                            payload["messages"] = [{"type": "text", "text": "輸入的會員編號為空列表，請重新輸入："}]
                        del state[userid]
                    elif not check_customer(text):
                        payload["messages"] = [{"type": "text", "text": "您輸入的顧客編號不存在，請重新輸入："}]
                    elif re.match(r"^[58]\d{3}$", text):
                        state[userid]["customer_list"].append(text)
                        print(text)
                        payload["messages"] = [{"type": "text", "text": "請繼續輸入顧客編號，若不再輸入請輸入 end 結束："}]
                elif text == "庫存查詢":
                    state[userid] = {"status": "awaiting_product_id"}
                    payload["messages"] = [{"type": "text", "text": "請輸入要查詢產品編號 :"}]
                elif state.get(userid) and state[userid]["status"] == "awaiting_product_id":
                    product_id = text.strip()
                    state[userid]["product_id"] = product_id
                    state[userid]["status"] = "awaiting_quantity_change"
                    payload["messages"] = [{"type": "text", "text": f"請輸入要修改的數量，若不需修改請輸入 '0'："}]
                    # payload["messages"] = [purchase_template(int(12), int(10))]
                elif state.get(userid) and state[userid]["status"] == "awaiting_quantity_change":
                    quantity = text
                    if text != "無":
                        quantity = int(text.strip())
                    product_id = state[userid]["product_id"]
                    payload["messages"] = [purchase_template(product_id, quantity)]
                    del state[userid]
                elif text == "銷售量預測":
                    payload["messages"] = [dashboard()]
                elif text == "交易紀錄":
                    global date, stime, etime
                    state[userid] = {"status": "awaiting_date"}
                    payload["messages"] = [picker()]
                else:
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            }
                        ]
                replyMessage(payload)
            
            # 處理座標訊息
            elif events[0]["message"]["type"] == "location":
                latitude = events[0]["message"]["latitude"]
                longitude = events[0]["message"]["longitude"]
                payload["messages"] = [get_navigation(latitude, longitude)]
                replyMessage(payload)
        
        elif events[0]["type"] == "postback":
            data = events[0]["postback"]["data"]
            if data == "rfm_pdf":
                payload["messages"] = [rfm_pdf_template(file_ad)]
            elif data == "store_info":
                payload["messages"] = [store_information()]
            elif state.get(userid) and state[userid]["status"] == "awaiting_date":
                if re.match(r"^\d{4}-\d{2}-\d{2}$", events[0]["postback"]["params"]["date"]):
                    date = events[0]["postback"]["params"]["date"]
                    state[userid]["status"] = "awaiting_start_time"
                    payload["messages"] = [picker_start()]
                else:
                    print(data["params"]["date"])
            elif state.get(userid) and state[userid]["status"] == "awaiting_start_time":
                if re.match(r"^(0[6-9]|1[0-9]|20):[0-5][0-9]$", events[0]["postback"]["params"]["time"]):                           
                    stime = events[0]["postback"]["params"]["time"]
                    state[userid]["status"] = "awaiting_end_time"
                    payload["messages"] = [picker_end()]
            elif state.get(userid) and state[userid]["status"] == "awaiting_end_time":
                if re.match(r"^(0[6-9]|1[0-9]|20):[0-5][0-9]$", events[0]["postback"]["params"]["time"]):
                    etime = events[0]["postback"]["params"]["time"]
                    state[userid]["status"] = "sale_over"
                    payload["messages"] = [salesreciepts_template(date, stime, etime)]
            replyMessage(payload)

    return 'OK'

def replyMessage(payload):
    print(payload)
    response = requests.post("https://api.line.me/v2/bot/message/reply",headers=HEADER,json=payload)
    print(response.text)
    return 'OK'
def pushMessage(payload):
    print(payload)
    response = requests.post("https://api.line.me/v2/bot/message/push",headers=HEADER,json=payload)
    print(response.text)
    return 'OK'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] #在request.headers拿到X-Line-Signature
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/order_post", methods=["GET", "POST"]) 
def order_post():
    request_method = request.method
    if request_method == "GET":
        userid = 'Ub7626e192b3edeb51c2560dd43bb2a82'
        return render_template('order.html', userid=userid)
    if request_method == "POST":
        customer_id = request.form.get("customer_id")
        product_category = request.form.get("product_category")
        product_name = request.form.get("product_name")
        quantity = request.form.get("quantity")
        print(customer_id, product_category, product_name, quantity)
        load=[customer_id,product_category,product_name,quantity]
        webform.writedata(load)

        total_price = webform.showtotal()
        return render_template('finish_order.html', data=load[0], total_price=total_price)

if __name__ == "__main__":
    app.debug = True
    app.run()