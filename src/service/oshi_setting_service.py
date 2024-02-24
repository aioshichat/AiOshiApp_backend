from flask import Response, json, request
from models.oshi_settings import OshiSetting
from models.database import db

def get_oshi_setting(oshi_setting_id):

    try:
    
        # 推し設定項目取得
        oshi_setting, err = OshiSetting.get_oshi_setting(oshi_setting_id)
        if err != None:
            return Response(response=json.dumps({
                "api_code": 400,
                "api_message": err,
            }), status=400)

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
        })


        return Response(response=response, status=200)
    
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }), status=500)
    

def update_oshi_setting(oshi_setting_id):

    try:
        # request bodyからデータ取得
        request_data = request.json
            
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
            }), status=400)


        return Response(response=json.dumps({
                "api_code": 200,
                "api_message": "OK!",
            }), status=200)
    
    except Exception as err:
        print(err)
        return Response(response=json.dumps({
            "api_code": 500,
            "api_message": "Server Internal Error",
        }), status=500)
    