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
base_url = "https://889c-140-116-121-18.jp.ngrok.io"

machine = TocMachine(
    states=["user", "sci", "sciSearch", "test", "houseplant", "hpPet","hpReccomend", "hpNewbie", "hpAdvanced","lan", "lanSearch"],
    transitions=[
        { "trigger": "advance", "source": "user", "dest": "sci", "conditions": "is_going_to_sci",},
        { "trigger": "advance", "source": "sci", "dest": "sciSearch", "conditions": "is_going_to_sciSearch",},
        { "trigger": "advance", "source": "sciSearch", "dest": "sci", "conditions": "is_going_to_sciSearchAgain",},
        { "trigger": "advance", "source": "user", "dest": "houseplant", "conditions": "is_going_to_houseplant",},
        { "trigger": "advance", "source": "houseplant", "dest": "hpPet", "conditions": "is_going_to_hpPet",},
        { "trigger": "advance", "source": "hpPet", "dest": "hpReccomend", "conditions": "is_going_to_hpReccomend",},
        { "trigger": "advance", "source": "user", "dest": "hpNewbie", "conditions": "is_going_to_hpNewbie",},
        { "trigger": "advance", "source": "user", "dest": "hpAdvanced", "conditions": "is_going_to_hpAdvanced",},
        { "trigger": "advance", "source": "user", "dest": "lan", "conditions": "is_going_to_lan",},
        { "trigger": "advance", "source": "lan", "dest": "lanSearch", "conditions": "is_going_to_lanSearch",},
        { "trigger": "go_back", "source": ["sciSearch", "hpReccomend", "hpNewbie", "hpAdvanced", "lanSearch"], "dest": "user"},
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
            send_text_message(event.reply_token,
            '\U0001F335輸入"臺灣植物名錄"\n可查尋臺灣的現有的植物物種喔\n\n\U0001F335輸入"冷知識"\n可以學到一個植物的小小冷知識\n\n\U0001F335輸入"室內盆栽推薦"\n看了許多植物的知識後是不是也想種種看呢~\n\n\U0001F335輸入"花語"\n可查詢各種花背後的意含呦')

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
