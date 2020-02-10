from flask import jsonify

def fxmessage():
    return jsonify({
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "carousel",
    "contents": [
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "Arm Chair, White",
              "size": "xl",
              "weight": "bold",
              "wrap": True
            },
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "text",
                  "text": "$49",
                  "flex": 0,
                  "size": "xl",
                  "weight": "bold",
                  "wrap": True
                },
                {
                  "type": "text",
                  "text": ".99",
                  "flex": 0,
                  "size": "sm",
                  "weight": "bold",
                  "wrap": True
                }
              ]
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
              "action": {
                "type": "uri",
                "label": "Add to Cart",
                "uri": "https://linecorp.com"
              },
              "style": "primary"
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "Add to whishlist",
                "uri": "https://linecorp.com"
              }
            }
          ]
        }
      },
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_6_carousel.png",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "Metal Desk Lamp",
              "size": "xl",
              "weight": "bold",
              "wrap": True
            },
            {
              "type": "box",
              "layout": "baseline",
              "flex": 1,
              "contents": [
                {
                  "type": "text",
                  "text": "$11",
                  "flex": 0,
                  "size": "xl",
                  "weight": "bold",
                  "wrap": True
                },
                {
                  "type": "text",
                  "text": ".99",
                  "flex": 0,
                  "size": "sm",
                  "weight": "bold",
                  "wrap": True
                }
              ]
            },
            {
              "type": "text",
              "text": "Temporarily out of stock",
              "flex": 0,
              "margin": "md",
              "size": "xxs",
              "color": "#FF5551",
              "wrap": True
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
              "action": {
                "type": "uri",
                "label": "Add to Cart",
                "uri": "https://linecorp.com"
              },
              "flex": 2,
              "color": "#AAAAAA",
              "style": "primary"
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "Add to wish list",
                "uri": "https://linecorp.com"
              }
            }
          ]
        }
      },
      {
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "See more",
                "uri": "https://linecorp.com"
              },
              "flex": 1,
              "gravity": "center"
            }
          ]
        }
      }
    ]
  }
})