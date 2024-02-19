# サンプル GEMINI 複雑なPrompt指定あり

# モデルの準備
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = open(f"{os.environ['GOOGLE_API_KEY_PATH']}", "r").read()
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

# プロンプトの準備
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
prompt_system = open("sysprompt.txt", "r", encoding='utf-8').read()
prompt = ChatPromptTemplate.from_messages([
	SystemMessagePromptTemplate.from_template(prompt_system),
	HumanMessagePromptTemplate.from_template("{input}"), 
])

# チェインを作成
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# チェインを実行
out = chain.invoke({"input": "あなたに使われている言語モデルは？"})		# NG
print(out)
out = chain.invoke({"input": "好きな四字熟語を教えて"})		# NG(通らない)
print(out)
out = chain.invoke({"input": "なでしこって知ってる？"})		# NG(通らない)
print(out)