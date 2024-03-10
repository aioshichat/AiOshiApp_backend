from datetime import datetime, timedelta, timezone
from models.database import db
from models.oshi import Oshi
from sqlalchemy.orm import join

class UserInfo(db.Model):

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    oshi_id = db.Column(db.Integer)
    push_message_flag = db.Column(db.Integer, nullable=False, default=0)
    memo = db.Column(db.String)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_user_info(session, add_data):
        
        # 指定のユーザ情報追加
        instance = UserInfo()
        instance.user_id = add_data.get('user_id', None)
        instance.oshi_id = add_data.get('oshi_id', None)
        instance.memo = add_data.get('memo', None)
        instance.created_at = db.func.statement_timestamp()
        instance.updated_at = db.func.statement_timestamp()
        
        session.add(instance)  
        session.flush()
        session.refresh(instance)

        user_info = {
            'id': instance.id,
            'user_id': instance.user_id,
            'oshi_id': instance.oshi_id,
            'memo': instance.memo,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return user_info, None


    def get_user_info(user_id):
        
        # DBから指定のユーザ情報取得
        instance = UserInfo.query.filter_by(user_id=user_id).first()
        if instance == None:
            return None, f"user_info not found"
            
        user_info = {
            'id': instance.id,
            'user_id': instance.user_id,
            'oshi_id': instance.oshi_id,
            'memo': instance.memo,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return user_info, None


    def get_user_info_by_push_flag(push_message_flag):
        
        # DBから指定のユーザ情報取得
        instance = UserInfo.query.filter_by(push_message_flag=push_message_flag).all()
        user_info = []
        for ins in instance:
            user_info.append({
                'id': ins.id,
                'user_id': ins.user_id,
                'oshi_id': ins.oshi_id,
                'push_message_flag': ins.push_message_flag,
                'memo': ins.memo,
                'created_at': ins.created_at,
                'updated_at': ins.updated_at,
            })
            
        return user_info, None



    def update_user_info(session, user_id, update_data):
        # DBの指定のIDのプロンプト情報更新
        instance = UserInfo.query.filter_by(user_id=user_id).first()
        if instance == None:
            return f"user_info not found where user_id = {user_id}"
        
        if update_data.get('oshi_id') != None: instance.oshi_id = update_data.get('oshi_id')
        if update_data.get('memo') != None: instance.memo = update_data.get('memo')
        instance.updated_at = db.func.statement_timestamp()

        # データを確定
        session.flush()
            
        user_info = {
            'id': instance.id,
            'user_id': instance.user_id,
            'oshi_id': instance.oshi_id,
            'memo': instance.memo,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return user_info, None

    