from datetime import datetime, timedelta, timezone
from models.database import db

class UserInfo(db.Model):

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    oshi_id = db.Column(db.Integer)
    memo = db.Column(db.String)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def get_user_info(user_id):
        
        # DBから指定のユーザ情報取得
        instance = UserInfo.query.filter_by(user_id=user_id).first()
        if instance == None:
            return None, f"user not found"
            
        user = {
            'id': instance.id,
            'user_id': instance.user_id,
            'oshi_id': instance.oshi_id,
            'memo': instance.memo,
            'updated_at': instance.updated_at,
            'created_at': instance.created_at,
        }
            
        return user, None

    
    def add_user_info(add_data):
        
        # 指定のユーザ情報追加
        user = UserInfo()
        user.user_id = add_data.get('user_id', None)
        user.oshi_id = add_data.get('oshi_id', None)
        user.memo = add_data.get('memo', None)
        
        db.session.add(user)  
        db.session.commit()
            
        return None
    