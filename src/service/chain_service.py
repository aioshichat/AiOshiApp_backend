import os
from flask import Response, json, request
from langchain.memory import ConversationBufferMemory
from models.database import db
from models.oshi_prompts import OshiPrompt
from models.user_info import UserInfo
from models.oshi import Oshi
from models.oshi_memories import OshiMemory
from controllers import ai_chain
from service import data_service



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

    # memory作成
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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
    user_info, err = UserInfo.get_user_info(user_id)

    if user_info == None:
        # user_info情報が存在しない場合、DBリソースを生成し、プロンプトを反映
        _, _, _, _, err = data_service.add_initial_data(user_id, message)
        if err != None:
            raise Exception(err)

        response_message = '*** 推しAI設定を追加しました！ ***'
        return response_message


    # 推しID取得
    oshi_id = user_info["oshi_id"]

    PROMPT_JUDGE_STRING = os.environ.get('PROMPT_JUDGE_STRING', '# 推しの呼び名')
    if PROMPT_JUDGE_STRING in message:
        # message内容がプロンプト情報の場合、oshi_promptを更新する
        try:
            ## session生成
            session = db.session

            ## promptを更新 (chat内容から)
            _, err = OshiPrompt.update_oshi_prompt(session, oshi_id, {'prompt':message})
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

        
    # prompt情報取得oshi_prompt
    oshi_prompt, err = OshiPrompt.get_oshi_prompt(oshi_id)
    prompt_system = oshi_prompt["prompt"]

    # template作成
    template = "{input}"

    # 履歴情報の設定
    ## 履歴情報をDBから取得
    MEMORY_INVOKE_LIMIT = os.environ.get('MEMORY_INVOKE_LIMIT', 3)
    oshi_memories, err = OshiMemory.get_oshi_memory(oshi_id, MEMORY_INVOKE_LIMIT)
    ## 履歴情報のインスタンス作成
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    ## for文で履歴情報をmemory追加
    for oshi_memory in oshi_memories:   
        memory.save_context({'input': oshi_memory['input']}, {'output': oshi_memory['output']})

    out = None
    # APIを実行してAIからの回答を取得する
    obj = ai_chain.AIChain()
    out = obj.invoke_openai(prompt_system, template, message, memory)
    print(out)

    # 履歴情報を保存
    try:
        ## session生成
        session = db.session
        
        ## DBに今回の会話内容を追加
        oshi_memories, err = OshiMemory.add_oshi_memory(session, {'oshi_id': oshi_id, 'input': out['input'], 'output': out['text']})
        ## 上限件数以上のデータを古い順にDBから削除 
        MEMORY_DB_LIMIT = os.environ.get('MEMORY_DB_LIMIT', 20)
        oshi_memories, err = OshiMemory.delete_oshi_memory(session, oshi_id, MEMORY_DB_LIMIT)

        ## sessionをcommit
        session.commit()

    except Exception as err:
        session.rollback()
        print(err)

    finally:
        session.close()

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

    PROMPT_JUDGE_STRING = os.environ.get('PROMPT_JUDGE_STRING', '# 推しの呼び名')
    if PROMPT_JUDGE_STRING in message:
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
    oshi_prompt, err = OshiPrompt.get_oshi_prompt(oshi_id)
    prompt_system = oshi_prompt["prompt"]

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

