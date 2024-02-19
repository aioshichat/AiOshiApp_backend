# サンプル OPENAI Prompt指定あり1

# モデルの準備
import os 
from langchain_openai.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = open(f"{os.environ['OPENAI_API_KEY_PATH']}", "r").read()
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# プロンプトの準備
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
prompt = ChatPromptTemplate.from_messages([
	SystemMessagePromptTemplate.from_template("あなたは植物の専門家です。簡潔な回答を好みます。"),
	HumanMessagePromptTemplate.from_template("{input}"), 
])

# チェインを作成
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# チェインを実行
out = chain.invoke({"input": "なでしこって知ってる？"})
print(out)