from flask import Response, json, request
from models.prompts import Prompt
from controllers import ai_chain



def invoke_common_logic(invoke_func):
    # クエリパラメータからデータ取得
    prompt_id = request.args.get("prompt_id", 0)
    send_message = request.args.get("send_message", None)

    # send_message未指定ならエラーを返す
    if send_message == None:
        return Response(response=json.dumps({
            "code": 400,
            "error_message": "parameter not found in query: send_message"
        }), status=400)

    # prompt情報取得
    prompt_system, err = Prompt.get_prompt_tmp(prompt_id)
    if err != None:
        return Response(response=json.dumps({
            "code": 400,
            "error_message": err
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
        response_str = out["text"]
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "code": 500,
            "error_message": "Server Internal Error"
        }), status=500)


    return Response(response=json.dumps({
            "code": 200,
            "ai_response": response_str
        }), status=200)


def invoke_openai_logic():
    obj = ai_chain.AIChain()
    return invoke_common_logic(obj.invoke_openai)


def invoke_gemini_logic():
    obj = ai_chain.AIChain()
    return invoke_common_logic(obj.invoke_gemini)