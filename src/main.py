from controllers import ai_chain
import sys


print("*** start ***")

obj = ai_chain.AIChain()

args = sys.argv
if len(args) < 2 or args[1] == "1":
    print("*** Geminiを使用します ***")
    invoke = obj.invoke_gemini
elif args[1] == "2":
    print("*** OpenAIを使用します ***")
    invoke = obj.invoke_openai
else:
    exit("*** 引数が不正です: 1 or 2 を指定してください ***")


prompt_system = ""
template = "{input}"
# message = {"input":"私の名前は田中太郎です"},

i = 0
# 5回まで
while(i < 5):
    i += 1
    print(">> ",end='')
    input_string = input().strip()
    message = {"input": input_string}

    try:
        out = invoke(prompt_system, template, message)
        print(f'<< {out["text"]}')
    except Exception as err:
        print("*** エラーが発生しました。別の質問をしてみてください。 ***")
    
print("*** end ***")