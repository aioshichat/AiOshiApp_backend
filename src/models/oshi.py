from datetime import datetime, timedelta, timezone
from models.database import db

class Oshi(db.Model):

    __tablename__ = 'oshi'

    id = db.Column(db.Integer, primary_key=True)
    user_info_id = db.Column(db.Integer)
    memo = db.Column(db.String)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_oshi(session, add_data):
        
        # 指定のユーザ情報追加
        instance = Oshi()
        instance.user_info_id = add_data.get('user_info_id', None)
        instance.memo = add_data.get('memo', None)
        instance.created_at = db.func.statement_timestamp()
        instance.updated_at = db.func.statement_timestamp()
        
        session.add(instance)  
        session.flush()
        session.refresh(instance)

        oshi = {
            'id': instance.id,
            'user_info_id': instance.user_info_id,
            'memo': instance.memo,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return oshi, None


    def get_oshi(oshi_id):
        
        # DBから指定のユーザ情報取得
        instance = Oshi.query.filter_by(oshi_id=oshi_id).first()
        if instance == None:
            return None, f"oshi not found where oshi_id={oshi_id}"
            
        oshi = {
            'id': instance.id,
            'user_info_id': instance.user_info_id,
            'memo': instance.memo,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return oshi, None

    
    
    