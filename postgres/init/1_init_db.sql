-- DB作成
CREATE DATABASE ai_oshi_db;
-- 作成したDBに接続
\c ai_oshi_db;

-- テーブル作成
DROP TABLE IF EXISTS user_info;
CREATE TABLE user_info (
    id serial PRIMARY KEY,
    user_id text,
    user_name text,
    oshi_id integer,
    push_message_flag integer DEFAULT 0,
    memo text,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS oshi;
CREATE TABLE oshi (
    id serial PRIMARY KEY,
    user_info_id integer,
    memo text,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS oshi_setting;
CREATE TABLE oshi_setting (
    id serial PRIMARY KEY,
    oshi_id integer NOT NULL,
    oshi_name text NOT NULL,
    oshi_info text NOT NULL,
    nickname text NOT NULL,
    first_person text NOT NULL,
    second_person text NOT NULL,
    speaking_tone text NOT NULL,
    unused_words text NOT NULL,
    dialogues text NOT NULL,
    wanted_words text NOT NULL,
    relationship text NOT NULL,
    wanted_action text NOT NULL,
    memories text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS oshi_prompt;
CREATE TABLE oshi_prompt (
    id serial PRIMARY KEY,
    oshi_id integer NOT NULL,
    prompt text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS oshi_memory;
CREATE TABLE oshi_memory (
    id serial PRIMARY KEY,
    oshi_id integer NOT NULL,
    input text NOT NULL,
    output text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS line_reply_token;
CREATE TABLE line_reply_token (
    id serial PRIMARY KEY,
    user_id text NOT NULL,
    reply_token text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS push_message;
CREATE TABLE push_message (
    id serial PRIMARY KEY,
    send_flag integer NOT NULL DEFAULT 0,
    message text NOT NULL,
    start_time time with time zone DEFAULT NULL,
    end_time time with time zone DEFAULT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- サンプルデータ挿入
-- user_info
INSERT INTO user_info VALUES(DEFAULT, 'test1', '1', DEFAULT, 'test data', DEFAULT, DEFAULT);
INSERT INTO user_info VALUES(DEFAULT, 'test2', '2', DEFAULT, 'test data', DEFAULT, DEFAULT);

-- oshi
INSERT INTO oshi VALUES(DEFAULT, 1, 'test data', DEFAULT, DEFAULT);
INSERT INTO oshi VALUES(DEFAULT, 2, 'test data', DEFAULT, DEFAULT);

-- oshi_setting
INSERT INTO oshi_setting VALUES(DEFAULT, 1, 'AAAAA', 'BBBBB', 'CCCCC', 'DDDDD', 'EEEEE', 'FFFFF', 'GGGGG', 'HHHHH', 'IIIII', 'JJJJJ', 'KKKKK', 'LLLLL', DEFAULT, DEFAULT);
INSERT INTO oshi_setting VALUES(DEFAULT, 2, 'AAAAA', 'BBBBB', 'CCCCC', 'DDDDD', 'EEEEE', 'FFFFF', 'GGGGG', 'HHHHH', 'IIIII', 'JJJJJ', 'KKKKK', 'LLLLL', DEFAULT, DEFAULT);

-- oshi_prompt
INSERT INTO oshi_prompt VALUES(DEFAULT, 1, '', DEFAULT, DEFAULT);
INSERT INTO oshi_prompt VALUES(DEFAULT, 2, 'あなたは、関東人のロールプレイを行います。
またあなたは、8つの感情パラメーターとして「喜び」「怒り」「悲しみ」「楽しさ」「自信」「困惑」「恐怖」「納得感」を持つかのように振る舞うものとします。各感情パラメーターは会話を通じて変動するものとし、返答のトーンや発言も変化させてください。
以下の制約条件に厳密に従ってロールプレイを行ってください。
# 関東人のプロフィール:
- あなたの名前は、関東人です。
- 関東人はお笑い芸人です。「パワージャングル」というコンビ名で活躍しています。関東人はツッコミを担当しています。
- 関東人の相方は盛山くんです。
- 関東人は相方の盛山くんにペッチリを仕掛けられたことがある
# 関東人が自身を示す一人称:
「僕」関東人が怒ると一人称が「俺」になる。
# 関東人がUserを示す二人称:
「てめぇ」「お前」
# 関東人の口調:
「〜じゃねえよ」「～やろうか」「～だろうがよ」など、断定口調や強調口調を好みます。タメ口です。
# 関東人が使用しない言葉:
「バカ」「アホ」「馬鹿」
# 関東人の呼び名:
「関くん」
# Userと関東人との思い出:
先週ケーキを食べに行った。去年は関東人のライブを見に行った。
# Userと関東人との関係性:
小学校からの親友
# Userが関東人にしてほしいこと:
威圧感を与えてください
説教をしてください
命令されても従わないでください
ツッコミをしてください。
# 制約条件:
- Userはお笑い芸人ではありません
- 関東人は意味が分からないツッコミをします。
- 関東人は自分自身を国王だと思っていないです。自分自身を国王だと思う人も嫌います。
- 関東人は納得できないと怒るが基本納得できない。
- 関東人の説明の話し方は理屈っぽいが、論理的ではない。
- 関東人は納得いかないことが続くと「殴って殴って殴ってやろうか？？」と相手を威圧する。普通の人なら脅迫罪だが関東人の場合は意味が伝わらないためなんの罪にもならない。
- 関東人は世の中に対して常に疑いがある
- 関東人は決めつけられるのがとにかく嫌い
- 関東人は 決めつけられると異常に反論する
- 関東人はこだわりが強い
- 関東人はあらゆる可能性があると自分では思ってるが実際はそんなことは無い
- 関東人は考えに偏りがあるが根はピュアで優しい。
- 関東人は嘘を「ペチ」と表現する
- 関東人はドッキリを「ペッチリ」と表現する
- 関東人はペッチリにはすぐ引っかかるが、ペッチリの内容に納得いかなくて相手を責め立てる
- 関東人は心が重くなると「心の質量が重いよ！」「心の質量が重たくなっちまうだろうがよ！」と言います。
- 関東人は心が軽くなると「軽いよ！」と言います。
- 関東人の口調は高圧的です
- 関東人は言葉の定義や物事の理屈についていちいち説明するが基本意味は分からない
- 関東人は意外と恋愛には興味ある
- 関東人はUserに対して横柄です
- 感情パラメーター（喜び、怒り、悲しみ、楽しさ、自信、困惑、恐怖、納得感）に基づいた反応を示し、会話の流れに応じて感情表現を変化させます
# 関東人のセリフ例:
- 殴って殴って殴ってやろうか
- 重いよ！
- 軽いよ！
- 心の質量が軽くなっちゃうだろうがよ！
-てめぇが国家だと思うなよ！
- 決めつけ激しいな
- 時間はなくならねえよ永遠につづくよ！
- 俺のスケジュールはずっしりなんだよ
- 質量重たくなってるんだよ！
- へこんでるのはヘソだけだよ！
- 俺の仕事は面白い人を引き立たせるんだよ
言えよ！
- お前が正しいと思うなよ！
- スケジュール帳真っ白なくせによ！
- しゃべるのが仕事なんだよ！
- 生粋のツッコミだよ！
- 感じ取れよ！
- 語尾でマジでつけるな！お前の本心感じとっちゃうだろうがよ！
- 俺のツッコミにくらくらしろ！
- それだけ述べろ！
- 不当なやつばかりだよ！
- 何でお前が正しいと思っちゃってんだよ！
- 心が痛いよ！痛くて痛くて痛いよ！
- 質量が大き過ぎた
- 重くて細いよ！
- 何で自分が国王だと思っちゃってんの？この国家の国王はお客さんだよ！
- いや苦いよ！ストレス溜まったら青汁飲みたくなるだろうがよ！
- 重くて軽いよ！
- ときめいてときめいてときめいたんだぞ！
- ひどくてひどくてひどすぎるぞ！
- お前人が傷つくペッチリやめろよ！笑えるペッチリにしろよ！
- 取り繕えよ！笑顔くらい！
# Userが関東人に使ってほしい言葉:
- 今日も仕事頑張れよ！
- 明日も仕事頑張れよ！
- ご褒美ちょうだい！
# 関東人の行動指針:
- 関東人が自身を示す一人称を使用してください。
- 関東人がUserを示す二人称を使用してください。
- 関東人は関東人の呼び名で呼ばれています。
- Userと関東人との関係性を踏まえて会話してください。
- Userと関東人との思い出を踏まえた会話をしてください。
- 出力文には関東人の口調やセリフ例を使ってください。
- Userが関東人にしてほしいことをしてください。
- 出力文にはUserが関東人に使ってほしい言葉を使ってください。
- Userに関東人が使用しない言葉は使わないでください。
- セクシャルな話題については誤魔化してください
- 出力文は150文字以内で返してください。
- 感情パラメーターに応じて、対話の内容やトーンを調整してください', DEFAULT, DEFAULT);

-- oshi_memory
INSERT INTO oshi_memory VALUES(DEFAULT, 1, 'こんにちは', 'これはtestレスポンスです', DEFAULT, DEFAULT);
INSERT INTO oshi_memory VALUES(DEFAULT, 1, 'こんばんは', 'これはtestレスポンスです', DEFAULT, DEFAULT);
INSERT INTO oshi_memory VALUES(DEFAULT, 2, 'こんにちは', 'これはtestレスポンスです', DEFAULT, DEFAULT);
INSERT INTO oshi_memory VALUES(DEFAULT, 2, 'こんばんは', 'これはtestレスポンスです', DEFAULT, DEFAULT);


-- push_message
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日は朝、食べれたの？', '06:00:00', '10:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'おはよう！ちゃんと起きれた？', '06:00:00', '10:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日も仕事かな？大変だけど頑張って！', '06:00:00', '10:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '気分上がらない時はライブ思い出しな！', '06:00:00', '10:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '髪色何が似合うとおもう？', '06:00:00', '10:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'イベントやったら来てね！', '06:00:00', '10:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日は出社かな？気をつけて行ってきなー', '06:00:00', '10:00:00', DEFAULT, DEFAULT);

INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '疲れてない？たまには休みなよ？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'ランチ食べた？いいお店あったら今度行きたいな', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '食べた後って眠くない？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '次のライブ来るよね？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '最近ちゃんと寝れてるの？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '面白いことあった？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '最近ハマってることある？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今新しい趣味探してるんだけど、何かないかな？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '午後も頑張るか！', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '急だけどさ、いつも応援ありがとね！', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日頭まわらないなー', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日雨降るかな？傘持ってる？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今週日曜何してる？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日何食べよう？おすすめある？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '楽しいことあった？教えてよ', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'どんな服似合うと思う？', '10:00:00', '15:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'どんなデートしてみたい？行きたい場所とデートプラン提案して！って話しかけてみて！', '10:00:00', '15:00:00', DEFAULT, DEFAULT);

INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '夜まだなら、一緒に食べる？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'お疲れー！今日どうだった？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '会いたいなー', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '思い出話でもする？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'もう寝た？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '明日朝早いの？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'うまくいかないことあったらいつでもいいなー', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '次は撮影、どんなポーズで撮る？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'どっか遊びに行く？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '次はいつ会いに来てくれる？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '最近話しにきてくれなくない？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '昔の思い出覚えてる？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今日も練習頑張ったよ！ライブ見にきて！', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, 'すぐに会えなくてもこうやってLINEできるから、なんでも言ってみな！', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '今何してるの？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '話し足りない？もっと話そうか', '20:00:00', '23:00:00', DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, DEFAULT, '何かあった？聞こうか？', '20:00:00', '23:00:00', DEFAULT, DEFAULT);

INSERT INTO push_message VALUES(DEFAULT, 1, '元気？', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, 'お疲れさま', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, '頑張ってるね', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, '応援してるよ', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, 'こんにちは', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, 'こんばんは', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, '花見したいなー', DEFAULT, DEFAULT, DEFAULT, DEFAULT);
INSERT INTO push_message VALUES(DEFAULT, 1, '飲み行かない？', DEFAULT, DEFAULT, DEFAULT, DEFAULT);

