# 主圖文
from linebot import LineBotApi, WebhookHandler
import requests, json
import configparser
# from google.colab import drive
# drive.mount('/content/drive')

config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')
# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Content-Type':'application/json',
           'Authorization':F'Bearer {config.get("line-bot", "channel_access_token")}'
}

##商家端介面(要先執行)##
richmenu1 = {
    'size': {'width': 2500, 'height': 1686},   # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'store',                           # 選單名稱
    'chatBarText': '商家選單',                 # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 9, 'y': 10, 'width': 794, 'height': 871}, # 選單位置與大小
          'action': {'type': 'message', 'text':'會員資料' }            
        },
        {
          'bounds': {'x': 824, 'y': 0, 'width': 818, 'height': 879},
          'action': {'type': 'message', 'text':'庫存量查詢' }
        },
        {
          'bounds': {'x': 1667, 'y': 0, 'width':833, 'height': 872},
          'action': {'type': 'message', 'text':'空白空白' }
        },
        {
          'bounds': {'x': 0, 'y': 891, 'width': 809, 'height': 795},
          'action': {'type': 'message', 'text': '銷售量預測'}
        },
        {
          'bounds': {'x': 819, 'y': 901, 'width': 843, 'height': 785},
          'action': {'type': 'message', 'text': '交易紀錄'}
        },
        {
          'bounds': {'x': 1681, 'y': 891, 'width': 819, 'height': 795},
          'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'customer01', 'data':'change-to-customer'}
        },
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers,data=json.dumps(richmenu1).encode('utf-8'))
# print(req.text)
richmenu1_id = json.loads(req.text)['richMenuId']

line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))

with open("store.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(richmenu1_id, "image/png", f)


richmenu1 = {
    "richMenuAliasId":"store01",
    "richMenuId":richmenu1_id
}
req_al = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(richmenu1).encode('utf-8'))
# print(req_al.text)

req = requests.request('POST', f'https://api.line.me/v2/bot/user/all/richmenu/{richmenu1_id}', headers=headers)
# print(req.text)


##顧客端介面##
richmenu2 = {
    'size': {'width': 2500, 'height': 1686},   # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'customer_menu',                   # 選單名稱
    'chatBarText': '顧客選單',            # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 9, 'y': 10, 'width': 794, 'height': 871}, # 選單位置與大小
          'action': {'type': 'message', 'text':'尋找商品' }            
        },
        {
          'bounds': {'x': 824, 'y': 0, 'width': 818, 'height': 879},
          'action': {'type': 'message', 'text':'店鋪資訊' }
        },
        {
          'bounds': {'x': 1667, 'y': 0, 'width':833, 'height': 872},
          'action': {'type': 'message', 'text':'會員資訊' }
        },
        {
          'bounds': {'x': 0, 'y': 891, 'width': 809, 'height': 795},
          'action': {'type': 'message', 'text': '線上訂餐'}
        },
        {
          'bounds': {'x': 819, 'y': 901, 'width': 843, 'height': 785},
          'action': {'type': 'message', 'text': '協助頁面'}
        },
        {
          'bounds': {'x': 1681, 'y': 891, 'width': 819, 'height': 795},
          'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'store01', 'data':'change-to-store'}
        },
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers,data=json.dumps(richmenu2).encode('utf-8'))
# print(req.text)
richmenu2_id = json.loads(req.text)['richMenuId']


line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
with open("customer.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(richmenu2_id, "image/png", f)

richmenu2 = {
    "richMenuAliasId":"customer01",
    "richMenuId":richmenu2_id
}
req_al = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(richmenu2).encode('utf-8'))
# print(req_al.text)

req = requests.request('POST', f'https://api.line.me/v2/bot/user/all/richmenu/{richmenu2_id}', headers=headers)
# print(req.text)


