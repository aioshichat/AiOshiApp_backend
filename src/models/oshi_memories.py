from datetime import datetime, timedelta, timezone
from models.database import db
from sqlalchemy import asc, desc
from sqlalchemy.sql.functions import current_timestamp

class OshiMemory(db.Model):

    __tablename__ = 'oshi_memory'

    id = db.Column(db.Integer, primary_key=True)
    oshi_id = db.Column(db.Integer, nullable=False)
    input = db.Column(db.String, nullable=False)
    output = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo')))


    def add_oshi_memory(session, add_data):
        
        # 指定の会話履歴
        instance = OshiMemory()
        instance.oshi_id = add_data.get('oshi_id')
        instance.input = add_data.get('input', "")
        instance.output = add_data.get('output', "")
        instance.created_at = db.func.statement_timestamp()
        instance.update_at = db.func.statement_timestamp()
        
        session.add(instance)
        session.flush()
        session.refresh(instance)

        oshi_memory = {
            'id': instance.id,
            'oshi_id': instance.oshi_id,
            'input': instance.input,
            'output': instance.output,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
            
        return oshi_memory, None


    def get_oshi_memory(oshi_id, limit=3):
        # DBから指定の推しIDの会話履歴取得
        instance = OshiMemory.query.filter_by(oshi_id=oshi_id).order_by(desc(OshiMemory.created_at)).limit(limit).all()
        oshi_memories = []
        for ins in instance:
            oshi_memories.append({
                "input": ins.input,
                "output": ins.output,
            })
            
        return oshi_memories, None


    def delete_oshi_memory(session, oshi_id, offset):
        
        # 指定の会話履歴
        instance = OshiMemory.query.filter_by(oshi_id=oshi_id).order_by(desc(OshiMemory.created_at)).offset(offset).all()
        for ins in instance:
            session.delete(ins)

        session.flush()
        # session.refresh(instance)

        deleted_ids = []
        for ins in instance:
            deleted_ids.append({
                'id': ins.id,
            })
            
        return deleted_ids, None