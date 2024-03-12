import os
from datetime import datetime, timedelta, timezone
from models.database import db
from models.oshi import Oshi
from sqlalchemy.orm import join
from models.oshi_memories import OshiMemory
from sqlalchemy import asc, desc, or_, and_
from sqlalchemy.sql.expression import func

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

        # 3日前の日付時刻文字列を取得
        PUSH_TIME_START_DATE = int(os.environ.get("PUSH_TIME_START_DATE", 3))
        d_start = datetime.now() - timedelta(PUSH_TIME_START_DATE)
        d_start_str = d_start.strftime("%Y-%m-%d %H:%M:%S")
        print(d_start_str)

        PUSH_TIME_END_HOUR = int(os.environ.get("PUSH_TIME_END_HOUR", 3))
        d_end = datetime.now() - timedelta(PUSH_TIME_END_HOUR) / 24
        d_end_str = d_end.strftime("%Y-%m-%d %H:%M:%S")
        print(d_end_str)
        
        # DBから指定のユーザ情報取得
        instance1 = db.session.query(OshiMemory.oshi_id, func.count(OshiMemory.oshi_id)).filter(and_(OshiMemory.created_at >= d_start_str, OshiMemory.created_at <= d_end_str, OshiMemory.input != "")).group_by(OshiMemory.oshi_id).all()
        user_info = []
        for ins1 in instance1:
            instance2 = UserInfo.query.filter_by(push_message_flag=push_message_flag, oshi_id=ins1.oshi_id).first()
            if instance2 == None:
                continue

            user_info.append({
                'id': instance2.id,
                'user_id': instance2.user_id,
                'oshi_id': instance2.oshi_id,
                'push_message_flag': instance2.push_message_flag,
                'memo': instance2.memo,
                'created_at': instance2.created_at,
                'updated_at': instance2.updated_at,
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

    