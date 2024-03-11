import os
import requests
from flask import json

class LineAPI():

    def auth_access_token(access_token):

            # access_tokenを認証
            ## LiNE公式の認証APIを送信
            LINE_URL_AUTH = os.environ.get('LINE_URL_AUTH', 'https://api.line.me/oauth2/v2.1/verify')
            params = {'access_token':access_token}
            r = requests.get(LINE_URL_AUTH, params=params)

            ## ステータスコード確認
            if r.status_code == 400:
                json_data = r.json()
                print(json_data)
                return None, {
                    "api_code": 400,
                    "api_message": json_data["error_description"],
                }
            elif r.status_code != 200:
                print("Server Internl Error")
                return None, {
                    "api_code": 500,
                    "api_message": "Server Internal Error",
                }
            
            json_data = r.json()
            ## client_idとチャンネルIDが一致するか確認
            ### 開発の用途とは関係ないので、一旦コメントアウト
            # client_id = json_data["client_id"]
            # LINE_CHANNEL_ID = os.environ["LINE_CHANNEL_ID"]
            # if client_id != LINE_CHANNEL_ID:
            #     print(json_data)
            #     return None, {
            #         "api_code": 400, 
            #         "api_message": f"client_id not matched channel_id: {client_id}",
            #     }

            ## Access Tokenの有効期限が切れないか確認 (400エラーになるためこちらは実施しない)


            result = {
                "scope": json_data.get("scope"),
                "client_id": json_data.get("client_id"),
                "expires_in": json_data.get("expires_in"),
            }

            print("Auth OK!")

            return result, None




    def get_profile_access_token(access_token):

            # access_tokenからuser_idを取得
            ## LiNE公式のプロフィール参照APIを送信
            LINE_URL_PROFILE = os.environ.get('LINE_URL_PROFILE', 'https://api.line.me/v2/profile')
            headers = {'Authorization': f'Bearer {access_token}'}
            r = requests.get(LINE_URL_PROFILE, headers=headers)

            ## statusコード確認
            if r.status_code != 200:
                print("get profile failed from access token")
                return None, {
                    "api_code":400, 
                    "api_message":"get profile failed from access token",
                }

            ## user_id取得
            json_data = r.json()

            profile = {
                "userId": json_data.get("userId"),
                "displayName": json_data.get("displayName"),
                "pictureUrl": json_data.get("pictureUrl"),
                "statusMessage": json_data.get("statusMessage"),
            }

            print("Profile OK!")

            return profile, None



    def push_message(user_id, message_array):

            LINE_URL_MESSAGE_PUSH = os.environ.get('LINE_URL_MESSAGE_PUSH', 'https://api.line.me/v2/bot/message/push')
            LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "xxxxxx")
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}',
            }
            messages = []
            for message in message_array:
                messages.append({
                        "type":"text",
                        "text":message
                })

            data = json.dumps({
                "to": user_id,
                "messages":messages
            })      # ensure_ascii=Falseは指定しないこと (日本語送信時にエラーになるため。メッセージはちゃんと日本語で届く)
            r = requests.post(LINE_URL_MESSAGE_PUSH, headers=headers, data=data)

            print(f"push message: {data}")
            print(r)
            print(json_data := r.json())

            if r.status_code != requests.codes.ok:
                return json_data, "API error"


            return json_data, None