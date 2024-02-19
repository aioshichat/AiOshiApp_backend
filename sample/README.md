# サンプルファイル実行方法

## API KEYの設定
ルートディレクトリの`.secret`ディレクトリ内に、OpenAIおよびGeminiのAPIキーを記載したテキストファイルを格納してください。  
ファイル名は以下のように指定してください。  
- openai.txt
- gemini.txt

※備考  
APIキーは秘密情報のため、ローカルでのみ保管するものとしgitにはコミットしないようお願いします。


## 動作確認方法
### コンテナ起動
ルートディレクトリで以下のコマンドを実行する
- イメージのビルドをする場合  
  `docker compose up -d --build`
- イメージのビルドをしない場合  
  `docker compose up -d`

### コンテナアタッチ
以下のいずれかの方法でbackendコンテナにアタッチする
- VSCodeの左下のボタンをクリックし、「Attach to Running Container...」をクリックし、「backend」を選択する
- 以下のコマンドを実行する  
  `docker exec -it backend bash`

### サンプル実行
以下のコマンドでサンプルファイルを実行する
```
cd sample
python3 【サンプルファイル名】
```
例.  

`python3 sample_openai_001.py`


## ファイル説明
- sample_openapi_...: OpenAIのAPIを利用したサンプルファイル
- sample_gemini_...: GeminiのAPIを利用したサンプルファイル
- sysprompt.txt: 関東人(ジャルジャルのネタで登場する人)のプロンプト情報  
  →一部のサンプルファイルで使用