# 店家資訊選單
import requests
from linebot.models import *
from googlemaps import Client
import configparser

# Google Map API 設定
config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')
google_map_key = config.get('line-bot', 'google_map_key')
gmaps = Client(key=google_map_key)

# 店鋪資訊
def store_information():
    message = {
    "type": "template",
    "altText": "This is a buttons template",
    "template": {
        "type": "buttons",
        "thumbnailImageUrl": "https://www.da-vinci.com.tw/uploads/images/cache/c21bfcc8370a5692792b2afa36d44bff-1000x500c00-1-1.jpg",
        "title": "Tibame cafe",
        "text": "桃園市中壢區復興路46號9樓\n營業時間: 週一到週五09:00 ~ 18:00",
        "actions": [
        {
            "type": "uri",
            "label": "撥打電話",
            "uri": 'tel:0912345678'
        },
        {
            "type": "uri",
            "label": '開啟導航',
            "uri": 'line://nv/location'
        },
        {
            "type": "message",
            "label": '附近景點',
            "text": '附近景點'
        }
        ]
    }
}
    return message

# 協助頁面QA
def problem_information():
    message = {
        'type': 'flex',
        'altText': 'this is a flex message',
        'contents': {
            'type': 'carousel',
            'contents': [{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "協助頁面 QA",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": []
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "訂單問題",
          "text": "訂單問題"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "反饋問卷",
          "uri": "https://www.surveycake.com/s/baOwg"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}]
        }
    }
    return message

# 附近景點功能
def get_attractions():
        # 固定座標在 TibaMe (中壢)
        lat, lng = 24.9576403, 121.2224478

        # 使用 Google Maps API 搜尋目標座標半徑500公尺的五個景點
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'location': f'{lat},{lng}',
            'radius': 3000,
            'type': 'tourist_attraction',
            'language': 'zh-TW',
            'key': google_map_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        data['results'].sort(key=lambda x: x.get('rating', 0), reverse=True)

        if len(data['results']) == 0:
            # 如果找不到景點，回覆「附近沒有景點」的訊息
            message = {'type': 'text', 'text': '附近沒有景點'}
        else:
            columns = []
            for item in data['results'][:5]:
                rating = item.get('rating', '尚未評分')
                column = {
                    'thumbnailImageUrl': f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={item["photos"][0]["photo_reference"]}&key=AIzaSyDikEPQlTOovtwj8DRQZvTS59k_abijceY',
                    'title': item['name'],
                    'text': f'{rating}星，{item.get("user_ratings_total", "0")}則評論',
                    'actions': [
                        {'type': 'uri', 'label': '在地圖上檢視', 'uri': f"https://www.google.com.tw/maps/place/?q=place_id:{item['place_id']}"},
                    ]
                }
                columns.append(column)
            carousel_template = {'type': 'carousel', 'columns': columns}
            message = {
                'type': 'template',
                'altText': '以下是附近的五個景點：',
                'template': carousel_template
            }

        return message

# 開啟導航功能
def get_navigation(latitude, longitude):
    # 目標地址，這裡可以自己設定
    target_address = "桃園市中壢區中和路139號"

    # 使用 Google Maps Platform 的 Geocoding API 將目標地址轉換為座標
    target_location = gmaps.geocode(target_address)[0]['geometry']['location']
    target_latitude = target_location['lat']
    target_longitude = target_location['lng']

    # 使用 Google Maps Platform 的 Distance Matrix API 計算當前使用者座標和目標座標之間的距離和時間
    directions_result = gmaps.directions(
        (latitude, longitude),
        (target_latitude, target_longitude),
        mode="driving",
        language="zh-TW"
    )
    # 獲取路線總長度和總時間
    distance_km = directions_result[0]['legs'][0]['distance']['text']
    duration_min = directions_result[0]['legs'][0]['duration']['text']

    # 取得導航連結
    navi_link = f"https://www.google.com/maps/dir/?api=1&destination={target_address}"

    # 回傳導航訊息
    message = {
        "type": "text",
        "text": f"請點擊以下連結開啟 Google 導航：\n{navi_link}\n預計距離：{distance_km}，預計行車時間：{duration_min}"
    }
    return message

# 訂單問題回覆
def order_problem_template():
    message = {
            'type': 'flex',
            'altText': 'this is a flex message',
            'contents': 
        {
            "type": "carousel",
            "contents": [
            {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "size": "sm",
                    "wrap": True,
                    "text": "有提供無咖啡因的選項嗎？",
                    "margin": "xs",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "margin": "md",
                        "contents": [
                        {
                            "type": "text",
                            "text": "我們有無咖啡因的選項供應。您可以選擇使用無咖啡因咖啡豆，我們也提供各種茶類飲品，讓您享受無咖啡因的選擇。",
                            "wrap": True,
                            "color": "#8c8c8c",
                            "size": "xs"
                        }
                        ]
                    }
                    ]
                }
                    ],
                    "spacing": "sm",
                    "paddingAll": "13px"
                }
                },
                {
                    "type": "bubble",
                    "size": "kilo",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                        "type": "text",
                        "text": "你們的咖啡是怎麼烘焙的？",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "margin": "md",
                        "contents": [
                        {
                            "type": "text",
                            "text": "我們的咖啡豆來自精心挑選的咖啡莊園，烘焙師會根據咖啡豆的特性風味，以及客人口味偏好，進行精確的烘焙。",
                            "wrap": True,
                            "color": "#8c8c8c",
                            "size": "xs",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "有提供素食或者無麩質選項嗎？",
                "weight": "bold",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "我們菜單中有許多素食和無麩質選項，以滿足不同客人的飲食需求和喜好。",
                        "wrap": True,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "是否可在店內舉辦聚會或活動？",
                "size": "sm",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "我們歡迎舉辦各種聚會或私人活動。請提前與我們聯繫，我們將協助您安排場地和提供特別的菜單選項。",
                        "flex": 5,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "有接受信用卡或行動支付嗎？",
                "size": "sm",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "抱歉，我們目前僅接受現金付款。",
                        "color": "#8c8c8c",
                        "flex": 5,
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "spacing": "sm",
            "paddingAll": "13px"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "有提供無糖或低糖的甜點嗎？",
                "size": "sm",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "我們菜單中有提供無糖或低糖的甜點選項，提供給客人更健康的選擇。",
                        "flex": 5,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "paddingAll": "13px",
            "spacing": "sm"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "咖啡是使用有機豆子嗎？",
                "wrap": True,
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "我們致力於使用優質的有機咖啡豆，這些豆子種植時不使用化學肥料或農藥，以確保您享受到最天然和健康的咖啡。",
                        "color": "#8c8c8c",
                        "flex": 5,
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "paddingAll": "13px",
            "spacing": "sm"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "有提供外送服務嗎？",
                "size": "sm",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "因店內人手不足我們尚未提供外送的服務。",
                        "flex": 5,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "paddingAll": "13px",
            "spacing": "sm"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "咖啡有提供客製化的服務嗎？例如加入特定的配料或調整糖份？",
                "size": "sm",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "您可以選擇加入特定的配料，如焦糖、巧克力醬或香草糖漿，或者要求調整糖份。",
                        "flex": 5,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "paddingAll": "13px",
            "spacing": "sm"
        }
        },
        {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "咖啡廳有設置無障礙設施嗎？",
                "size": "sm",
                "weight": "bold",
                "wrap": True
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "我們的咖啡廳設有無障礙設施，包括無障礙廁所和輪椅通道。",
                        "flex": 5,
                        "color": "#8c8c8c",
                        "size": "xs",
                        "wrap": True
                    }
                    ]
                }
                ]
            }
            ],
            "paddingAll": "13px",
            "spacing": "sm"
        }
        }
    ]
    }
    }
    return message