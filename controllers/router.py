from flask import Blueprint
from service import chain_service
from service import oshi_setting_service

# Generate Router Instance
router = Blueprint('router', __name__)



# 推し設定項目
## 推し設定項目 取得
@router.route("/api/v1/oshi/settings/<oshi_setting_id>", methods=['GET'])
def func001(oshi_setting_id):
    return oshi_setting_service.get_oshi_setting(oshi_setting_id)

## 推し設定項目 設定
@router.route("/api/v1/oshi/settings/<oshi_setting_id>", methods=['POST'])
def func002(oshi_setting_id):
    return oshi_setting_service.update_oshi_setting(oshi_setting_id)



# AIへメッセージを送信
## OpenAI
@router.route("/api/v1/invokeOpenAI", methods=['POST'])
def invokeOpenAIAPI():
    return chain_service.invoke_openai_logic()

## Gemini
@router.route("/api/v1/invokeGemini", methods=['POST'])
def invokeGeminiAPI():
    return chain_service.invoke_gemini_logic()

