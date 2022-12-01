import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImagemapSendMessage
from linebot.models import *

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
BASEURL = "https://687e-140-116-121-18.jp.ngrok.io"


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

# def send_text_emoji(reply_token, text, e):
#     line_bot_api = LineBotApi(channel_access_token)
#     line_bot_api.reply_message(reply_token, TextSendMessage(text=text, emojis=e))
#     return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_imagemap(reply_token, url, c1, c2, c3, c4):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImagemapSendMessage(
        base_url = url,
        alt_text='this is an imagemap',
        base_size=BaseSize(height=1040, width=1040),
        actions=[
            MessageImagemapAction(
                text=c1,
                area=ImagemapArea(
                    x=0, y=0, width=520, height=520
                )
            ),
            MessageImagemapAction(
                text=c2,
                area=ImagemapArea(
                    x=520, y=0, width=520, height=520
                )
            ),
            MessageImagemapAction(
                text=c3,
                area=ImagemapArea(
                    x=0, y=520, width=520, height=520
                )
            ),
            MessageImagemapAction(
                text=c4,
                area=ImagemapArea(
                    x=520, y=520, width=520, height=520
                )
            )
        ]
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
