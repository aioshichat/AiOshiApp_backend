from datetime import datetime, timedelta, timezone
from models.database import db

class OshiSetting(db.Model):

    __tablename__ = 'oshi_setting'

    id = db.Column(db.Integer, primary_key=True)
    first_person = db.Column(db.String, nullable=False)
    called_name = db.Column(db.String, nullable=False)
    second_person = db.Column(db.String, nullable=False)
    tone = db.Column(db.String)
    forbidden_words = db.Column(db.String)
    memories = db.Column(db.String)
    relationship = db.Column(db.String, nullable=False)
    hopes = db.Column(db.String, nullable=False)
    additional_profile = db.Column(db.String)
    hope_words = db.Column(db.String)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def get_oshi_setting(oshi_setting_id):
        # DBから指定のユーザIDの設定情報取得

        instance = OshiSetting.query.filter_by(id=oshi_setting_id).first()
        if instance == None:
            return None, f"oshi_setting not found where oshi_setting_id = {oshi_setting_id}"

        array = {
            "first_person": instance.first_person,
            "called_name": instance.called_name,
            "second_person": instance.second_person,
            "tone": instance.tone,
            "forbidden_words": instance.forbidden_words,
            "memories": instance.memories,
            "relationship": instance.relationship,
            "hopes": instance.hopes,
            "additional_profile": instance.additional_profile,
            "hope_words": instance.hope_words,
        }
            
        return array, None


    def update_oshi_setting(oshi_setting_id, update_data):
        # DBの指定のユーザIDの設定情報更新
        instance = OshiSetting.query.filter_by(id=oshi_setting_id).first()
        if instance == None:
            return None, f"oshi_setting not found where oshi_setting_id = {oshi_setting_id}"
        
        instance.first_person = update_data["first_person"]
        instance.called_name = update_data["called_name"]
        instance.second_person = update_data["second_person"]
        instance.tone = update_data["tone"]
        instance.forbidden_words = update_data["forbidden_words"]
        instance.memories = update_data["memories"]
        instance.relationship = update_data["relationship"]
        instance.hopes = update_data["hopes"]
        instance.additional_profile = update_data["additional_profile"]
        instance.hope_words = update_data["hope_words"]

        # データを確定
        db.session.commit()
            
        return None
    