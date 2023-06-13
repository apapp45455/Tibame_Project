def member_template():
    message = {
        "type": "flex",
        "altText":'this is a message',
        "contents":{
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "會員專區",
                        "weight": "bold",
                        "size": "xl",
                        "style": "normal",
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
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
                            "label": "消費記錄",
                            "text": "消費記錄",
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": "點數 point",
                        "uri": "https://lin.ee/gnjG2ua"
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": "我的優惠卷",
                        "uri": "https://lin.ee/v8Kx1BT"
                        }
                    }
                    ],
                    "flex": 0
                        }
                        }
                        ]
                    }
            }
    return message

