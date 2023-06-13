def dashboard():
    message = {
        "type": "flex",
        "altText":'this is a message',
        "contents":{
            "type": "carousel",
            "contents": []
            }
    }
    message_iter = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://img.lovepik.com/element/45007/5009.png_300.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    },
    "align": "end",
    "gravity": "bottom",
    "margin": "none",
    "offsetTop": "none"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "報表幫手",
        "wrap": True,
        "weight": "bold",
        "gravity": "center",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "行銷人的好幫手",
                "color": "#210F18",
                "size": "sm",
                "flex": 1,
                "align": "center",
                "weight": "bold"
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "color": "#210F18"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "contents": [
          {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/linecorp_code_withborder.png",
            "aspectMode": "cover",
            "size": "xl",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "註：請妥善使用行銷工具",
            "color": "#aaaaaa",
            "wrap": True,
            "margin": "xxl",
            "size": "xs"
          }
        ]
      }
    ],
    "backgroundColor": "#F4E88E"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "進入儀表板",
          "uri": " https://0b26-111/order_post"
        },
        "style": "link"
      }
    ]
  }
}
    message['contents']['contents'].append(message_iter)
    return message