from datetime import datetime, timedelta, timezone
from models.database import db
from sqlalchemy import asc, desc

class PushMessage(db.Model):

    __tablename__ = 'push_message'

    id = db.Column(db.Integer, primary_key=True)
    send_flag = db.Column(db.Integer, nullable=False, default=0)
    message = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_push_message(session, add_data):
        
        # 指定のユーザ情報追加
        instance = PushMessage()
        instance.message = add_data.get('message', None)
        instance.created_at = db.func.statement_timestamp()
        instance.updated_at = db.func.statement_timestamp()
        
        session.add(instance)  
        session.flush()
        session.refresh(instance)

        user_info = {
            'id': instance.id,
            'send_flag': instance.send_flag,
            'message': instance.message,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return user_info, None


    def get_push_message_by_send_flag(send_flag):
        
        # DBから指定のユーザ情報取得
        instance = PushMessage.query.filter_by(send_flag=send_flag).order_by(asc(PushMessage.id)).limit(1).first()
        if instance == None:
            return None, f"push_message not found"
            
        push_message = {
            'id': instance.id,
            'send_flag': instance.send_flag,
            'message': instance.message,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return push_message, None

