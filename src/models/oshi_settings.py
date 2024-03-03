from datetime import datetime, timedelta, timezone
from models.database import db

class OshiSetting(db.Model):

    __tablename__ = 'oshi_setting'

    id = db.Column(db.Integer, primary_key=True)
    oshi_id = db.Column(db.Integer, unique=True, nullable=False)
    oshi_name = db.Column(db.String, nullable=False)
    oshi_info = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    first_person = db.Column(db.String, nullable=False)
    second_person = db.Column(db.String, nullable=False)
    speaking_tone = db.Column(db.String, nullable=False)
    unused_words = db.Column(db.String, nullable=False)
    dialogues = db.Column(db.String, nullable=False)
    wanted_words = db.Column(db.String, nullable=False)
    relationship = db.Column(db.String, nullable=False)
    wanted_action = db.Column(db.String, nullable=False)
    memories = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_oshi_setting(session, add_data):
        
        # 指定のユーザ情報追加
        instance = OshiSetting()
        instance.oshi_id = add_data['oshi_id']
        instance.oshi_name = add_data.get('oshi_name', '')
        instance.oshi_info = add_data.get('oshi_info', '')
        instance.nickname = add_data.get('nickname', '')
        instance.first_person = add_data.get('first_person', '')
        instance.second_person = add_data.get('second_person', '')
        instance.speaking_tone = add_data.get('speaking_tone', '')
        instance.unused_words = add_data.get('unused_words', '')
        instance.dialogues = add_data.get('dialogues', '')
        instance.wanted_words = add_data.get('wanted_words', '')
        instance.relationship = add_data.get('relationship', '')
        instance.wanted_action = add_data.get('wanted_action', '')
        instance.memories = add_data.get('memories', '')
        instance.created_at = db.func.statement_timestamp()
        instance.updated_at = db.func.statement_timestamp()
        
        session.add(instance)  
        session.flush()
        session.refresh(instance)

        oshi_setting = {
            "id": instance.id,
            "oshi_id": instance.oshi_id,
            "oshi_name": instance.oshi_name,
            "oshi_info": instance.oshi_info,
            "nickname": instance.nickname,
            "first_person": instance.first_person,
            "second_person": instance.second_person,
            "speaking_tone": instance.speaking_tone,
            "unused_words": instance.unused_words,
            "dialogues": instance.dialogues,
            "wanted_words": instance.wanted_words,
            "relationship": instance.relationship,
            "wanted_action": instance.wanted_action,
            "memories": instance.memories,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
            
        return oshi_setting, None


    def get_oshi_setting(oshi_id):
        # DBから指定の推しIDの設定情報取得

        instance = OshiSetting.query.filter_by(oshi_id=oshi_id).first()
        if instance == None:
            return None, f"oshi_setting not found where oshi_id = {oshi_id}"

        oshi_setting = {
            "id": instance.id,
            "oshi_id": instance.oshi_id,
            "oshi_name": instance.oshi_name,
            "oshi_info": instance.oshi_info,
            "nickname": instance.nickname,
            "first_person": instance.first_person,
            "second_person": instance.second_person,
            "speaking_tone": instance.speaking_tone,
            "unused_words": instance.unused_words,
            "dialogues": instance.dialogues,
            "wanted_words": instance.wanted_words,
            "relationship": instance.relationship,
            "wanted_action": instance.wanted_action,
            "memories": instance.memories,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
            
        return oshi_setting, None


    def update_oshi_setting(session, oshi_id, update_data):
        # DBの指定の推しIDの設定情報更新
        instance = OshiSetting.query.filter_by(oshi_id=oshi_id).first()
        if instance == None:
            return None, f"oshi_setting not found where oshi_id = {oshi_id}"
        
        if update_data.get("oshi_name") != None: instance.oshi_name = update_data["oshi_name"]
        if update_data.get("oshi_info") != None: instance.oshi_info = update_data["oshi_info"]
        if update_data.get("nickname") != None: instance.nickname = update_data["nickname"]
        if update_data.get("first_person") != None: instance.first_person = update_data["first_person"]
        if update_data.get("second_person") != None: instance.second_person = update_data["second_person"]
        if update_data.get("speaking_tone") != None: instance.speaking_tone = update_data["speaking_tone"]
        if update_data.get("unused_words") != None: instance.unused_words = update_data["unused_words"]
        if update_data.get("dialogues") != None: instance.dialogues = update_data["dialogues"]
        if update_data.get("wanted_words") != None: instance.wanted_words = update_data["wanted_words"]
        if update_data.get("relationship") != None: instance.relationship = update_data["relationship"]
        if update_data.get("wanted_action") != None: instance.wanted_action = update_data["wanted_action"]
        if update_data.get("memories") != None: instance.memories = update_data["memories"]
        instance.updated_at = db.func.statement_timestamp()

        # データを確定
        session.flush()

        oshi_setting = {
            "id": instance.id,
            "oshi_id": instance.oshi_id,
            "oshi_name": instance.oshi_name,
            "oshi_info": instance.oshi_info,
            "nickname": instance.nickname,
            "first_person": instance.first_person,
            "second_person": instance.second_person,
            "speaking_tone": instance.speaking_tone,
            "unused_words": instance.unused_words,
            "dialogues": instance.dialogues,
            "wanted_words": instance.wanted_words,
            "relationship": instance.relationship,
            "wanted_action": instance.wanted_action,
            "memories": instance.memories,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
            
        return oshi_setting, None
    