import os
from flask import Response, json, request
from models.oshi_prompts import OshiPrompt
from models.user_info import UserInfo
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
        }, ensure_ascii=False), status=400)

    # prompt情報取得
    prompt_system, err = OshiPrompt.get_oshi_prompt(oshi_id)
    if err != None:
        return Response(response=json.dumps({
            "api_code": 400,
            "api_message": err,
        }, ensure_ascii=False), status=400)

    # template作成
    template = "{input}"

    # message作成
    message = {"input": send_message}

    out = None
    try:
        # APIを実行してAIからの回答を取得する
        out = invoke_func(prompt_system, template, message)
        print(out)
        received_message = out["text"].encode().decode('utf-8')
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }, ensure_ascii=False), status=500)


    return Response(response=json.dumps({
            "api_code": 200,
            "api_message": "OK!",
            "received_message": received_message,
        }, ensure_ascii=False), status=200)


def invoke_openai_logic():
    obj = ai_chain.AIChain()
    return invoke_common_logic(obj.invoke_openai)


def invoke_gemini_logic():
    obj = ai_chain.AIChain()
    return invoke_common_logic(obj.invoke_gemini)




def invoke_openai_logic_line(user_id, message):
    # user_idに紐づくoshi_idを取得
    # TODO: user_idは個人情報かもなのでハッシュ化したほうが良いかも
    user, err = UserInfo.get_user_info(user_id)
    if err != None:
        # user情報が存在しない場合、ユーザを追加しoshi_idに0に指定
        UserInfo.add_user_info({'user_id':user_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}'})
        oshi_id = None
    else: 
        oshi_id = user["oshi_id"]

    # prompt情報取得
    prompt_system, err = OshiPrompt.get_oshi_prompt(oshi_id)
    if oshi_id == None or err != None:
        # prompt情報が存在しない場合、空白文字を指定
        prompt_system = ""

    # template作成
    template = "{input}"

    # message作成
    # message = {"input": send_message}

    out = None
    # APIを実行してAIからの回答を取得する
    obj = ai_chain.AIChain()
    out = obj.invoke_openai(prompt_system, template, message)
    print(out)
    received_message = out["text"]
    return received_message


def invoke_gemini_logic_line(user_id, message):
    # user_idに紐づくoshi_idを取得
    # TODO: user_idは個人情報かもなのでハッシュ化したほうが良いかも
    user, err = UserInfo.get_user_info(user_id)
    if err != None:
        # user情報が存在しない場合、ユーザを追加しoshi_idに0に指定
        UserInfo.add_user_info({'user_id':user_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}'})
        oshi_id = None
    else: 
        oshi_id = user["oshi_id"]

    # prompt情報取得
    prompt_system, err = OshiPrompt.get_oshi_prompt(oshi_id)
    if oshi_id == None or err != None:
        # prompt情報が存在しない場合、空白文字を指定
        prompt_system = ""

    # template作成
    template = "{input}"

    # message作成
    # message = {"input": send_message}

    out = None
    # APIを実行してAIからの回答を取得する
    obj = ai_chain.AIChain()
    out = obj.invoke_gemini(prompt_system, template, message)
    print(out)
    received_message = out["text"]
    return received_message

