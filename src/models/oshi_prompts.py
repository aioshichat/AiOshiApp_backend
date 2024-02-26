from datetime import datetime, timedelta, timezone
from models.database import db

class OshiPrompt(db.Model):

    __tablename__ = 'oshi_prompt'

    id = db.Column(db.Integer, primary_key=True)
    oshi_id = db.Column(db.Integer, unique=True, nullable=False)
    prompt = db.Column(db.String)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_oshi_prompt(session, add_data):
        
        # 指定のユーザ情報追加
        instance = OshiPrompt()
        instance.oshi_id = add_data.get('oshi_id', None)
        instance.prompt = add_data.get('prompt', None)
        
        session.add(instance)  
        session.flush()
        session.refresh(instance)

        oshi_prompt = {
            'id': instance.id,
            'oshi_id': instance.oshi_id,
            'prompt': instance.prompt,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return oshi_prompt, None
    
    
    def get_oshi_prompt(oshi_id):
        
        if oshi_id == 0:
            # 関東人のprompt情報をファイルから取得
            prompt_system = open("models/sysprompt_sekitoto.txt", "r", encoding='utf-8').read()
        else:
            # DBから指定の推しIDのプロンプト情報取得
            instance = OshiPrompt.query.filter_by(oshi_id=oshi_id).first()
            if instance == None:
                return None, f"oshi_prompt not found where oshi_id = {oshi_id}"
                
            prompt_system = instance.prompt
            
        return prompt_system, None


    def update_oshi_prompt(session, oshi_id, update_data):
        # DBの指定のIDのプロンプト情報更新
        instance = OshiPrompt.query.filter_by(oshi_id=oshi_id).first()
        if instance == None:
            return f"oshi_prompt not found where oshi_id = {oshi_id}"
        
        if update_data.get('prompt') != None: instance.prompt = update_data.get('prompt')

        # データを確定
        session.flush()
            
        return None

    