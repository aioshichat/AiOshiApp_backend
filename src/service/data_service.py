import os
from flask import Response, json, request
from models.database import db
from models.user_info import UserInfo
from models.oshi import Oshi
from models.oshi_settings import OshiSetting
from models.oshi_prompts import OshiPrompt
from models.oshi_memories import OshiMemory
from controllers import ai_chain
from langchain.memory import ConversationBufferMemory




def add_initial_data(user_id, message=""):
    # user_idから各テーブルの基本データを生成
    # TODO: user_idは個人情報かもなのでハッシュ化したほうが良いかも
    try:
        ## session生成
        session = db.session

        ## user_infoを生成
        user_info, err = UserInfo.add_user_info(session, {'user_id':user_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}()'})
        user_info_id = user_info['id']
        ## oshiを生成
        oshi, err = Oshi.add_oshi(session, {'user_info_id':user_info_id, 'memo':f'added in {os.sys._getframe().f_code.co_name}()'})
        oshi_id = oshi['id']
        ## user_infoの有効oshi_idを更新
        user_info, err = UserInfo.update_user_info(session, user_id, {'oshi_id':oshi_id})
        ## oshi_settingを生成
        oshi_setting, err = OshiSetting.add_oshi_setting(session, {'oshi_id':oshi_id})
        ## oshi_promptを生成
        oshi_prompt, err = OshiPrompt.add_oshi_prompt(session, {'oshi_id':oshi_id, 'prompt':message})

        ## sessionをcommit
        session.commit()

        return user_info, oshi, oshi_setting, oshi_prompt, None

    except Exception as err:
        session.rollback()
        return None, None, None, None, err

    finally:
        session.close()



def generate_episode_by_memory(oshi_name, relationship, memories):
    try:
        # 指定の文字列から、エピソードを生成する
        ## AIに送信するメッセージ生成
        message = f'''\
以下の情報から、楽しかったエピソード2つ、面白かったエピソード2つ、悲しかったエピソード2つ作って

# Userと{oshi_name}との関係性:
{relationship}
# User目線の{oshi_name}との思い出:
{memories}'''

        ## prompt_system生成
        prompt_system = ""
        ## template作成
        template = "{input}"
        ## 履歴情報のインスタンス作成
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        ## APIを実行してAIからの回答を取得する
        obj = ai_chain.AIChain()
        out = obj.invoke_openai(prompt_system, template, message, memory)
        print(out)
        received_message = out["text"]

        return received_message, None
    
    except Exception as err:
        print(err)
        return None, err

