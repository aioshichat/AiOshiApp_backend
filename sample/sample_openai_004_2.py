# サンプル OPENAI 複雑なPrompt指定あり(関東人) メモリあり

# モデルの準備
import os 
from langchain_openai.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = open(f"{os.environ['OPENAI_API_KEY_PATH']}", "r").read()
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# プロンプトの準備
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate,)
from langchain.prompts import MessagesPlaceholder

prompt_system = open("sysprompt.txt", "r", encoding='utf-8').read()
prompt = ChatPromptTemplate.from_messages([
	SystemMessagePromptTemplate.from_template(prompt_system),
	MessagesPlaceholder(variable_name="chat_history"),
	HumanMessagePromptTemplate.from_template("{input}"), 
])

# チェインを作成
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)

# チェインを実行
out = chain.invoke({"input": "私の名前は田中太郎です"})
print(out)

out = chain.invoke({"input": "私の名前を言ってみてください"})
print(out)