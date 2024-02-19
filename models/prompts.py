

class Prompt():

    def __init__():
        return

    def get_prompt_tmp(prompt_id):
        # 関東人のprompt情報をファイルから取得
        # TODO: DBからの取得処理は今後別バックログで対応予定

        prompt_system = None
        err = None
        if prompt_id == "0":
            prompt_system = ""
        elif prompt_id == "1":
            prompt_system = open("models/sysprompt_sekitoto.txt", "r", encoding='utf-8').read()
        else:
            err = f"prompt not found where prompt_id = {prompt_id}"
            
        return prompt_system, err
    