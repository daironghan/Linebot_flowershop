import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()
base_url = "https://1bc6-140-116-121-18.jp.ngrok.io"

machine = TocMachine(
    states=["user", "houseplant", "hpReccomend", "hpNewbie", "hpAdvanced","lan", "lanSearch"],
    transitions=[
        { "trigger": "advance", "source": "user", "dest": "houseplant", "conditions": "is_going_to_houseplant",},
        { "trigger": "advance", "source": "houseplant", "dest": "hpReccomend", "conditions": "is_going_to_hpReccomend",},
        { "trigger": "advance", "source": "user", "dest": "hpNewbie", "conditions": "is_going_to_hpNewbie",},
        { "trigger": "advance", "source": "user", "dest": "hpAdvanced", "conditions": "is_going_to_hpAdvanced",},
        { "trigger": "advance", "source": "user", "dest": "lan", "conditions": "is_going_to_lan",},
        { "trigger": "advance", "source": "lan", "dest": "lanSearch", "conditions": "is_going_to_lanSearch",},
        { "trigger": "go_back", "source": ["hpReccomend", "hpNewbie", "hpAdvanced", "lanSearch"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)



@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        print(f'\nFSM STATE: {machine.state}')

        response = True
        if event.message.text.lower() == 'fsm':
            send_image_message(event.reply_token, f'{base_url}/fsm') # route
        else:
            response = machine.advance(event)

        if response == False:
            send_text_message(event.reply_token,'\U0001F335輸入"花語"\n可查詢各種花背後的意含\n\n\U0001F335輸入"盆栽推薦"\n可幫助想種植物但不之從哪裡開始的人呦')

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
