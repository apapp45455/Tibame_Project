import configparser
config = configparser.ConfigParser() #讀取config檔案
config.read('config.ini')
end_point = config.get('line-bot', 'end_point')

def product_template():
        message = {
            'type': 'flex',
            'altText': 'this is a flex message',
            'contents': 
        {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "尋找商品",
        "weight": "bold",
        "size": "xl",
        "wrap": False,
        "style": "normal",
        "position": "relative",
        "align": "center"
      },
      {
        "type": "separator",
        "color": "#688e26"
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
          "label": "價目表",
          "text": "價目表"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "精選商品",
          "text": "精選商品"
        }
      }
    ],
    "flex": 0
  }
}
        }
        return message

def product_type():
        message = {
            'type': 'flex',
            'altText': 'this is a flex message',
            'contents': 
        {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "價目表",
        "weight": "bold",
        "size": "xl",
        "wrap": False,
        "style": "normal",
        "position": "relative",
        "align": "center"
      },
      {
        "type": "separator",
        "color": "#688e26"
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
          "label": "咖啡豆",
          "text": "咖啡豆"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "茶飲",
          "text": "茶飲"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "咖啡",
          "text": "咖啡"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "甜品",
          "text": "甜品"
        }
      }
    ],
    "flex": 0
  }
}
        }
        return message

def getImageMessage(originalContentUrl):
    message = dict()
    message["type"] = "image"
    message["originalContentUrl"] = originalContentUrl
    message["previewImageUrl"] = originalContentUrl
    return message

def bean_menu():
    originalContentUrl=F"{end_point}/static/coffee_beans_menu.png"
    return getImageMessage(originalContentUrl)
def tea_menu():
    originalContentUrl=F"{end_point}/static/tea_menu.png"
    return getImageMessage(originalContentUrl)      
def coffee_menu():
    originalContentUrl=F"{end_point}/static/coffee_menu.png"
    return getImageMessage(originalContentUrl)
def bakery_menu():
    originalContentUrl=F"{end_point}/static/bakery_menu.png"
    return getImageMessage(originalContentUrl)