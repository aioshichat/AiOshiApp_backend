import os
from flask import Blueprint, abort, request
from service import chain_service
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, Source, TextMessage, TextSendMessage

# Generate Router Instance
router = Blueprint('router_line', __name__)

if not (access_token := os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")

if not (channel_secret := os.environ.get("LINE_CHANNEL_SECRET")):
    raise Exception("channel secret is not set as an environment variable")

line_bot_api = LineBotApi(access_token)
handler_openai = WebhookHandler(channel_secret)
handler_gemini = WebhookHandler(channel_secret)


# AIへメッセージを送信
## OpenAI
@router.route("/lineapi/v1/invokeOpenAI", methods=["POST"])
def invokeOpenAIAPI() -> str:
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)

    try:
        print(body)
        handler_openai.handle(body, signature)
    except InvalidSignatureError as err:
        print(err)
        abort(400)

    return "OK"

## Gemini
@router.route("/lineapi/v1/invokeGemini", methods=["POST"])
def invokeGeminiAPI() -> str:
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)

    try:
        print(body)
        handler_gemini.handle(body, signature)
    except Exception as err:
        print(err)
        abort(400)

    return "OK"


@handler_openai.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent) -> None:
    text_message: TextMessage = event.message
    source: Source = event.source
    user_id: str = source.user_id

    res_text: str = chain_service.invoke_openai_logic_line(user_id, text_message.text)

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=res_text.strip())
    )


@handler_gemini.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent) -> None:
    text_message: TextMessage = event.message
    source: Source = event.source
    user_id: str = source.user_id

    res_text: str = chain_service.invoke_gemini_logic_line(user_id, text_message.text)

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=res_text.strip())
    )