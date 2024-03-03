from datetime import datetime, timedelta, timezone, timedelta
from models.database import db

class LineReplyToken(db.Model):

    __tablename__ = 'line_reply_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    reply_token = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_line_reply_token(session, add_data):
        
        # 指定のreply_token追加
        instance = LineReplyToken()
        instance.user_id = add_data.get('user_id')
        instance.reply_token = add_data.get('reply_token')
        instance.created_at = db.func.statement_timestamp()
        instance.updated_at = db.func.statement_timestamp()
        
        session.add(instance)  
        session.flush()
        session.refresh(instance)

        line_reply_token = {
            'id': instance.id,
            'user_id': instance.user_id,
            'reply_token': instance.reply_token,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return line_reply_token, None
    
    
    def get_line_reply_token(reply_token):
        
        instance = LineReplyToken.query.filter_by(reply_token=reply_token).all()
                
        line_reply_token = []
        for ins in instance:
            line_reply_token.append({
                "id":ins.id
            })
            
        return line_reply_token, None


    def delete_line_reply_token_past_24hours(session):

        # 24時間前の日付時刻文字列を取得
        d = datetime.now() - timedelta(1)
        d_str = d.strftime("%Y-%m-%d %I:%M:%S")
        
        # 指定の会話履歴
        instance = LineReplyToken.query.filter(LineReplyToken.created_at <= d_str).all()
        for ins in instance:
            session.delete(ins)

        session.flush()

        deleted_ids = []
        for ins in instance:
            deleted_ids.append({
                'id': ins.id,
            })
            
        return deleted_ids, None

    