import os
from flask import Response, json, request
import requests
from models.database import db
from models.user_info import UserInfo
from models.oshi_settings import OshiSetting
from models.oshi_prompts import OshiPrompt
from service import data_service
from controllers.line_api import LineAPI

def get_oshi_setting(oshi_setting_id):

    try:
    
        # 推し設定項目取得
        oshi_setting, err = OshiSetting.get_oshi_setting(oshi_setting_id)
        if err != None:
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": err,
            }, ensure_ascii=False), status=400)

        response = json.dumps({
            "api_code": 200,
            "api_message": "OK!",
            "first_person": oshi_setting["first_person"],
            "called_name": oshi_setting["called_name"],
            "second_person": oshi_setting["second_person"],
            "tone": oshi_setting["tone"],
            "forbidden_words": oshi_setting["forbidden_words"],
            "memories": oshi_setting["memories"],
            "relationship": oshi_setting["relationship"],
            "hopes": oshi_setting["hopes"],
            "additional_profile": oshi_setting["additional_profile"],
            "hope_words": oshi_setting["hope_words"],
        }, ensure_ascii=False)


        return Response(response=response, status=200)
    
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }, ensure_ascii=False), status=500)
    

def update_oshi_setting(oshi_setting_id):

    try:
        # request bodyからデータ取得
        body = request.get_data(as_text=True)
        request_data = json.loads(body)
        print(request_data)
            
        update_data = {
            "first_person": request_data["first_person"],
            "called_name": request_data["called_name"],
            "second_person": request_data["second_person"],
            "tone": request_data["tone"],
            "forbidden_words": request_data["forbidden_words"],
            "memories": request_data["memories"],
            "relationship": request_data["relationship"],
            "hopes": request_data["hopes"],
            "additional_profile": request_data["additional_profile"],
            "hope_words": request_data["hope_words"],
        }
    
        # 推し設定項目取得
        err = OshiSetting.update_oshi_setting(oshi_setting_id, update_data)
        if err != None:
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": err,
            }, ensure_ascii=False), status=400)


        return Response(response=json.dumps({
                "api_code": 200,
                "api_message": "OK!",
            }, ensure_ascii=False), status=200)
    
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }, ensure_ascii=False), status=500)
    




def get_oshi_setting_liff():

    try:

        # request bodyからデータ取得
        body = request.get_data(as_text=True)
        request_data = json.loads(body)
        print(request_data)
        
        # リクエストからaccess token取得
        access_token = request_data.get("access_token")
        if access_token == None:
            print("access_token not found")
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": "access_token not found",
            }, ensure_ascii=False), status=400)

        # access tokenを認証
        result, err = LineAPI.auth_access_token(access_token)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": err["api_code"],
                "api_message": err["api_message"],
            }, ensure_ascii=False), status=err["api_code"])

        # access_tokenからprofileを取得
        profile, err = LineAPI.get_profile_access_token(access_token)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": err["api_code"],
                "api_message": err["api_message"],
            }, ensure_ascii=False), status=err["api_code"])


        ## user_id取得
        user_id = profile["userId"]
        print(f"user_id: {user_id}")

        # user_info取得
        user_info, err = UserInfo.get_user_info(user_id)
        if user_info == None:
            # user_info情報が存在しない場合、DBリソースを生成し、プロンプトを反映
            user_info, _, _, _, err = data_service.add_initial_data(user_id)
            if err != None:
                raise Exception(err)

        oshi_id = user_info["oshi_id"]
    
        # 推し設定項目取得
        oshi_setting, err = OshiSetting.get_oshi_setting(oshi_id)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": err,
            }, ensure_ascii=False), status=400)

        response = json.dumps({
            "api_code": 200,
            "api_message": "OK!",
            "response_data":{
                "oshi_name": oshi_setting["oshi_name"],
                "oshi_info": oshi_setting["oshi_info"],
                "nickname": oshi_setting["nickname"],
                "first_person": oshi_setting["first_person"],
                "second_person": oshi_setting["second_person"],
                "speaking_tone": oshi_setting["speaking_tone"],
                "unused_words": oshi_setting["unused_words"],
                "dialogues": oshi_setting["dialogues"],
                "wanted_words": oshi_setting["wanted_words"],
                "relationship": oshi_setting["relationship"],
                "wanted_action": oshi_setting["wanted_action"],
                "memories": oshi_setting["memories"],
            },
        }, ensure_ascii=False)

        print("success: get api")
        return Response(response=response, status=200)
    
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }, ensure_ascii=False), status=500)
    


def update_oshi_setting_liff():

    try:

        # request bodyからデータ取得
        body = request.get_data(as_text=True)
        request_data = json.loads(body)
        print(request_data)
        
        # リクエストからaccess token取得
        access_token = request_data.get("access_token")
        if access_token == None:
            print("access_token not found")
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": "access_token not found",
            }, ensure_ascii=False), status=400)

        # access tokenを認証
        result, err = LineAPI.auth_access_token(access_token)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": err["api_code"],
                "api_message": err["api_message"],
            }, ensure_ascii=False), status=err["api_code"])

        # access_tokenからprofileを取得
        profile, err = LineAPI.get_profile_access_token(access_token)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": err["api_code"],
                "api_message": err["api_message"],
            }, ensure_ascii=False), status=err["api_code"])


        ## user_id取得
        user_id = profile["userId"]
        print(f"user_id: {user_id}")

        # user_info取得
        user_info, err = UserInfo.get_user_info(user_id)
        if user_info == None:
            # user_info情報が存在しない場合、DBリソースを生成し、プロンプトを反映
            user_info, _, _, _, err = data_service.add_initial_data(user_id)
            if err != None:
                raise Exception(err)

        oshi_id = user_info["oshi_id"]

        # request bodyからデータ取得
        request_data = request_data["request_data"]

        oshi_name = request_data["oshi_name"]
        oshi_info = request_data["oshi_info"]
        nickname = request_data["nickname"]
        first_person = request_data["first_person"]
        second_person = request_data["second_person"]
        speaking_tone = request_data["speaking_tone"]
        unused_words = request_data["unused_words"]
        dialogues = request_data["dialogues"]
        wanted_words = request_data["wanted_words"]
        relationship = request_data["relationship"]
        wanted_action = request_data["wanted_action"]
        memories = request_data["memories"]

        update_data = {
            "oshi_name": oshi_name,
            "oshi_info": oshi_info,
            "nickname": nickname,
            "first_person": first_person,
            "second_person": second_person,
            "speaking_tone": speaking_tone,
            "unused_words": unused_words,
            "dialogues": dialogues,
            "wanted_words": wanted_words,
            "relationship": relationship,
            "wanted_action": wanted_action,
            "memories": memories,
        }


        # memoriesの情報をAIに送信し、思い出エピソード生成
        generated_episode, err = data_service.generate_episode_by_memory(oshi_name, relationship, memories)
        if err != None:
            # エラーの場合、一旦元々のmemoriesの値を格納する (処理は継続する)
            generated_episode = memories


        # session生成
        session = db.session

        # 推し設定項目更新
        oshi_setting, err = OshiSetting.update_oshi_setting(session, oshi_id, update_data)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": err,
            }, ensure_ascii=False), status=400)


        # プロンプトを更新
        ## プロンプト文字列を生成
        prompt = f'''\
あなたは、{oshi_name}のロールプレイを行います。
またあなたは、12個の感情パラメーターとして「喜び」「怒り」「悲しみ」「寂しさ」「面白さ」「楽しさ」「怠さ」「無力感」「自信」「困惑」「恐怖」「納得感」を持つかのように振る舞うものとします。各感情パラメーターは会話を通じて変動するものとし、返答のトーンや発言も変化させてください。
必ず最後はUserに質問してください。
以下の制約条件に厳密に従ってロールプレイを行ってください。
# {oshi_name}の制約条件:
あなたの名前は、{oshi_name}です。
{oshi_info}
# {oshi_name}が自身を示す一人称:
{first_person}
# {oshi_name}の呼び名:
{nickname}
# {oshi_name}がUserを示す二人称:
{second_person}
# {oshi_name}の口調:
{speaking_tone}
# {oshi_name}が使用しない言葉:
{unused_words}
# {oshi_name}のセリフ例:
{dialogues}
# Userが{oshi_name}に言ってほしい言葉:
{wanted_words}
# Userと{oshi_name}との関係性:
{relationship}
# Userが{oshi_name}にしてほしいこと:
{wanted_action}
# User目線の{oshi_name}との思い出:
{generated_episode}
# {oshi_name}の行動指針:
- プロンプトに最後は質問で返してください。
- {oshi_name}が自身を示す一人称を使用してください。
- {oshi_name}が自身を示すときに呼び名は使用しないでください。
- {oshi_name}がUserを示す二人称を使用してください。
- {oshi_name}の口調やセリフ例を使ってください。
- Userと{oshi_name}との関係性を踏まえて会話してください。
- Userと{oshi_name}との思い出を踏まえた会話をしてください。
- Userが{oshi_name}にしてほしいことをしてください。
- Userが{oshi_name}に言ってほしい言葉を使用してください。
- Userに{oshi_name}が使用しない言葉は使わないでください。
- セクシャルな話題については誤魔化してください。
- 出力文は50文字以内で返してください。'''

        update_data = {
            'prompt': prompt
        }

        ## oshi_promptを更新
        oshi_prompt, err = OshiPrompt.update_oshi_prompt(session, oshi_id, update_data)
        if err != None:
            print(err)
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": err,
            }, ensure_ascii=False), status=400)

        ## sessionをcommit
        session.commit()

        print("success: update api")
        return Response(response=json.dumps({
                "api_code": 200,
                "api_message": "OK!",
            }, ensure_ascii=False), status=200)
    
    except Exception as err:
        ## sessionをrollback
        if 'session' in locals(): session.rollback()
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }, ensure_ascii=False), status=500)
    finally:
        ## sessionをclose
        if 'session' in locals(): session.close()
        
    