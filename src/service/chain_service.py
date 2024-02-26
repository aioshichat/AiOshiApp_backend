import os
from flask import Response, json, request
from models.database import db
from models.oshi_prompts import OshiPrompt
from models.user_info import UserInfo
from models.oshi import Oshi
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
    user_info, err = UserInfo.get_user_info(user_id)
    if user_info == None:
        # user_info情報が存在しない場合、DBリソースを生成し、プロンプトを反映
        try:
            ## session生成
            session = db.session

            ## user_infoを生成
            user_info, err = UserInfo.add_user_info(session, {'user_id':user_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}()'})
            user_info_id = user_info['id']
            ## oshiを生成
            oshi, err = Oshi.add_oshi(session, {'user_info_id':user_info_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}()'})
            oshi_id = oshi['id']
            ## user_infoのoshi_idを更新
            err = UserInfo.update_user_info(session, user_id, {'oshi_id':oshi_id})
            ## promptを生成 (chat内容から)
            oshi_prompt, err = OshiPrompt.add_oshi_prompt(session, {'oshi_id':oshi_id, 'prompt':message})

            ## sessionをcommit
            session.commit()

            response_message = '*** 推しAI設定を追加しました！ ***'
            return response_message

        except Exception as err:
            session.rollback()
            raise Exception(err)

        finally:
            session.close()


    # 推しID取得
    oshi_id = user_info["oshi_id"]

    if '# 推しの呼び名' in message:
        # message内容がプロンプト情報の場合、oshi_promptを更新する
        try:
            ## session生成
            session = db.session

            ## promptを更新 (chat内容から)
            err = OshiPrompt.update_oshi_prompt(session, oshi_id, {'prompt':message})
            if err != None:
                raise Exception(err)

            ## sessionをcommit
            session.commit()

            response_message = '*** 推しAI設定を更新しました！ ***'
            return response_message
            
        except Exception as err:
            session.rollback()
            raise Exception(err)

        finally:
            session.close()

        
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
    user_info, err = UserInfo.get_user_info(user_id)
    if user_info == None:
        # user_info情報が存在しない場合、DBリソースを生成し、プロンプトを反映
        try:
            ## session生成
            session = db.session

            ## user_infoを生成
            user_info, err = UserInfo.add_user_info(session, {'user_id':user_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}()'})
            user_info_id = user_info['id']
            ## oshiを生成
            oshi, err = Oshi.add_oshi(session, {'user_info_id':user_info_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}()'})
            oshi_id = oshi['id']
            ## user_infoのoshi_idを更新
            err = UserInfo.update_user_info(session, user_id, {'oshi_id':oshi_id})
            ## promptを生成 (chat内容から)
            oshi_prompt, err = OshiPrompt.add_oshi_prompt(session, {'oshi_id':oshi_id, 'prompt':message})

            ## sessionをcommit
            session.commit()

            response_message = '*** 推しAI設定を追加しました！ ***'
            return response_message

        except Exception as err:
            session.rollback()
            raise Exception(err)

        finally:
            session.close()


    # 推しID取得
    oshi_id = user_info["oshi_id"]

    if '# 推しの呼び名' in message:
        # message内容がプロンプト情報の場合、oshi_promptを更新する
        try:
            ## session生成
            session = db.session

            ## promptを更新 (chat内容から)
            err = OshiPrompt.update_oshi_prompt(session, oshi_id, {'prompt':message})
            if err != None:
                raise Exception(err)

            ## sessionをcommit
            session.commit()

            response_message = '*** 推しAI設定を更新しました！ ***'
            return response_message
            
        except Exception as err:
            session.rollback()
            raise Exception(err)

        finally:
            session.close()

        
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

