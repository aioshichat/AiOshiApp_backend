from flask import Response, json, request
from models.oshi_prompts import OshiPrompt
from controllers import ai_chain



def invoke_common_logic(invoke_func):
    # request bodyからデータ取得
    request_data = request.json

    oshi_id = request_data.get("oshi_id", 0)
    send_message = request_data.get("send_message", None)

    # send_message未指定ならエラーを返す
    if send_message == None:
        return Response(response=json.dumps({
            "api_code": 400,
            "api_message": "parameter not found in query: send_message",
        }), status=400)

    # prompt情報取得
    prompt_system, err = OshiPrompt.get_oshi_prompt(oshi_id)
    if err != None:
        return Response(response=json.dumps({
            "api_code": 400,
            "api_message": err,
        }), status=400)

    # template作成
    template = "{input}"

    # message作成
    message = {"input": send_message}

    out = None
    try:
        # APIを実行してAIからの回答を取得する
        out = invoke_func(prompt_system, template, message)
        print(out)
        received_message = out["text"]
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }), status=500)


    return Response(response=json.dumps({
            "api_code": 200,
            "api_message": "OK!",
            "received_message": received_message,
        }), status=200)


def invoke_openai_logic():
    obj = ai_chain.AIChain()
    return invoke_common_logic(obj.invoke_openai)


def invoke_gemini_logic():
    obj = ai_chain.AIChain()
    return invoke_common_logic(obj.invoke_gemini)