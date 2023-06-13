def memberdata():
    message = {
        "type": "flex",
        "altText":'this is a flex message',
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
                        "text": "會員資料",
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
                            "label": "查詢會員資訊",
                            "text": "查詢會員資訊",
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "顧客分群",
                            "data": "rfm_pdf",
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