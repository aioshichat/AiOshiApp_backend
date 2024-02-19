# サンプル OPENAI 複雑なPrompt指定あり(関東人)

# モデルの準備
import os 
from langchain_openai.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = open(f"{os.environ['OPENAI_API_KEY_PATH']}", "r").read()
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

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
out = chain.invoke({"input": "なでしこって知ってる？"})
print(out)