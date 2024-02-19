from flask import Blueprint
from service import chain_service

# Generate Router Instance
router = Blueprint('router', __name__)


@router.route("/api/v1/invokeOpenAI", methods=['GET'])
def invokeOpenAIAPI():
    return chain_service.invoke_openai_logic()


@router.route("/api/v1/invokeGemini", methods=['GET'])
def invokeGeminiAPI():
    return chain_service.invoke_gemini_logic()