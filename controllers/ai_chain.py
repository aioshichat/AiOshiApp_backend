import os 
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

class AIChain:

    def __init__(self):
        # OpenAIのAPIキー取得
        os.environ["OPENAI_API_KEY"] = open(f"{os.environ['OPENAI_API_KEY_PATH']}", "r").read()
        os.environ["GOOGLE_API_KEY"] = open(f"{os.environ['GOOGLE_API_KEY_PATH']}", "r").read()


    def invoke_openai(self, prompt_system="", template="{input}", message=""):
        # LLM作成
        llm = ChatOpenAI(model_name=f"{os.environ['OPENAI_VERSION']}", temperature=0)
        # プロンプトの準備
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_system),
            HumanMessagePromptTemplate.from_template(template), 
        ])

        # chain生成
        chain = LLMChain(llm=llm, prompt=prompt)

        # チェインを実行：APIを実行して応答を受け取る
        out = chain.invoke(message)

        return out


    def invoke_gemini(self, prompt_system="", template="{input}", message=""):
        # LLM作成
        llm = ChatGoogleGenerativeAI(model=f"{os.environ['GEMINI_VERSION']}", convert_system_message_to_human=True)
        # プロンプトの準備
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_system),
            HumanMessagePromptTemplate.from_template(template), 
        ])

        # chain生成
        chain = LLMChain(llm=llm, prompt=prompt)

        # チェインを実行：APIを実行して応答を受け取る
        out = chain.invoke(message)

        return out



