def picker_start():
    message = {
        "type": "flex",
        "altText":'this is a flex message',
        "contents":{
            "type": "carousel",
            "contents": []
            }
    }
    message_iter = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "aspectMode": "cover",
    "url": "https://media0.giphy.com/media/Js1mGOG7W1zsnkqmtk/giphy.gif"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "請輸入起始時間",
        "weight": "bold",
        "size": "xl",
        "align": "center"
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
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "datetimepicker",
          "label": "action",
          "data": "start_time",
          "mode": "time"
        }
      }
    ],
    "flex": 0
  }
}
    message['contents']['contents'].append(message_iter)
    return message

def picker_end():
    message = {
        "type": "flex",
        "altText":'this is a flex message',
        "contents":{
            "type": "carousel",
            "contents": []
            }
    }
    message_iter = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "aspectMode": "cover",
    "url": "https://media0.giphy.com/media/Js1mGOG7W1zsnkqmtk/giphy.gif"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "請輸入結束時間",
        "weight": "bold",
        "size": "xl",
        "align": "center"
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
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "datetimepicker",
          "label": "action",
          "data": "end_time",
          "mode": "time"
        }
      }
    ],
    "flex": 0
  }
}
    message['contents']['contents'].append(message_iter)
    return message

def picker():
    message = {
        "type": "flex",
        "altText":'this is a flex message',
        "contents":{
            "type": "carousel",
            "contents": []
            }
    }
    message_iter = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "aspectMode": "cover",
    "url": "https://media0.giphy.com/media/Js1mGOG7W1zsnkqmtk/giphy.gif"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "請輸入日期",
        "weight": "bold",
        "size": "xl",
        "align": "center"
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
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "datetimepicker",
          "label": "action",
          "data": "date",
          "mode": "date"
        }
      }
    ],
    "flex": 0
  }
}
    message['contents']['contents'].append(message_iter)
    return message