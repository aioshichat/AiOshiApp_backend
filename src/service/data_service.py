import os
from flask import Response, json, request
from models.database import db
from models.user_info import UserInfo
from models.oshi import Oshi
from models.oshi_settings import OshiSetting
from models.oshi_prompts import OshiPrompt
from models.oshi_memories import OshiMemory




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

