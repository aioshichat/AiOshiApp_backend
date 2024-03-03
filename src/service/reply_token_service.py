from models.line_reply_token import LineReplyToken
from models.database import db


def is_reply_token_exists(reply_token):
    
    ## DBにreply_tokenがあるか確認
    line_reply_token, err = LineReplyToken.get_line_reply_token(reply_token)

    is_exists = False
    ## 存在する場合、True
    if line_reply_token != None and len(line_reply_token) >= 1:
        is_exists = True

    return is_exists


def update_reply_token(user_id, reply_token):

    try :
        session = db.session

        ## 24時間以上前のreply_token削除
        line_reply_token, err = LineReplyToken.delete_line_reply_token_past_24hours(session)
        ## 今回のreply_token追加
        line_reply_token, err = LineReplyToken.add_line_reply_token(session, {"user_id":user_id, "reply_token":reply_token})

        session.commit()

        return

    except Exception as err:
        print(err)
    
    finally:
        session.close()
