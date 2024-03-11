import sys, os
sys.path.append("/usr/src")
from flask import Flask
from controllers.line_api import LineAPI
from models.database import db, init_db
from models.user_info import UserInfo
from models.push_messages import PushMessage
from models.oshi_memories import OshiMemory
import random
import time


# 送信時間をずらすため、ランダム分数sleepを挟む
t = random.randrange(30)
# time.sleep(t * 60)

# app = Flask(__name__)
# app.config.from_object('models.config.Config')
# init_db(app)
# # app.test_request_context().push()
# app.app_context().push()


# # DBからpush message対象のユーザ一覧を取得
# user_info, err = UserInfo.get_user_info_by_push_flag(1)
# print(user_info)

# # 各ユーザ宛のメッセージ取得
# push_message, err = PushMessage.get_push_message_by_send_flag(0)
# if err != None:
#     print(f"error: {err}")
#     print("failed to execute push message job.")
#     exit(-1)
# print(push_message)

# 各ユーザにメッセージ送信
i = 0
# for user in user_info:
#     user_id = user["user_id"]
#     message = push_message["message"]
#     message_array = [
#         message,
#     ]
#     # メッセージ送信
#     res, err = LineAPI.push_message(user_id, message_array)
#     if err != None:
#         print(err)
#         continue

#     # 会話履歴更新
#     try:
#         ## session生成
#         session = db.session

#         oshi_id = user["oshi_id"]
#         ## DBに今回の会話内容を追加
#         oshi_memories, err = OshiMemory.add_oshi_memory(session, {'oshi_id': oshi_id, 'input': "", 'output': message})
#         ## 上限件数以上のデータを古い順にDBから削除 
#         MEMORY_DB_LIMIT = os.environ.get('MEMORY_DB_LIMIT', 20)
#         oshi_memories, err = OshiMemory.delete_oshi_memory(session, oshi_id, MEMORY_DB_LIMIT)

#         ## sessionをcommit
#         session.commit()

#     except Exception as err:
#         session.rollback()
#         print(err)

#     finally:
#         session.close()
    
#     i += 1

# print(f"push message count: {i}")
exit(i)