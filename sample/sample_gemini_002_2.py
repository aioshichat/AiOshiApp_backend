# サンプル GEMINI Prompt指定あり2

# モデルの準備
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = open(f"{os.environ['GOOGLE_API_KEY_PATH']}", "r").read()
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

# プロンプトの準備
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
prompt = ChatPromptTemplate.from_messages([
	SystemMessagePromptTemplate.from_template("あなたはプログラミング言語の専門家です。簡潔な回答を好みます。"),
	HumanMessagePromptTemplate.from_template("{input}"), 
])

# チェインを作成
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# チェインを実行
out = chain.invoke({"input": "あなたに使われている言語モデルは？"})		# OK
print(out)
out = chain.invoke({"input": "好きな四字熟語を教えて"})		# OK
print(out)
out = chain.invoke({"input": "なでしこって知ってる？"})		# OK
print(out)