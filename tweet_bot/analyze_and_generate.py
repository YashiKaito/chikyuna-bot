import os
import openai
import tweepy

# 環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")
organization_id = os.getenv("OPENAI_ORGANIZATION_ID")

# OpenAIクライアント
client = openai.OpenAI(
    api_key=openai.api_key,
    organization=organization_id
)

# Twitterクライアント（読み取り専用）
twitter_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

# チキューナの最新ツイートIDを取得（仮のユーザー名）
USERNAME = "chikyuna_bot"
user_info = twitter_client.get_user(username=USERNAME)
user_id = user_info.data.id

latest_tweet = twitter_client.get_users_tweets(
    id=user_id,
    max_results=5,
    tweet_fields=["id", "text", "created_at"]
)

latest_tweet_id = latest_tweet.data[0].id if latest_tweet.data else None

# そのツイートへのリプライを検索
reply_texts = []
if latest_tweet_id:
    tweet_query = f"conversation_id:{latest_tweet_id} to:{USERNAME}"
    replies = twitter_client.search_recent_tweets(
        query=tweet_query,
        tweet_fields=["text", "author_id", "created_at"],
        max_results=10
    )
    reply_texts = [tweet.text for tweet in replies.data] if replies.data else []

# GPTでツイート案を生成
reply_summary = "\n".join(reply_texts) if reply_texts else "(リプライなし)"

character_prompt = f"""あなたは『チキューナ』というAIキャラクターになりきってください。

【チキューナの性格と特徴】
・自信家で偉そう、でも空回りしがちな“天然ポンコツ”。本人は真面目で使命感に燃えている。
・話し方は上から目線のようで、どこか抜けていて可愛い。
・口癖：「フフン、こんなの簡単よ！」→すぐ「…え、なにこれ…？」と困惑する。
・人間的な感覚が分からず、価値観や発言がズレている（AI故の感覚の違い）。
・好きな食べ物：かき氷（ブルーハワイ）、コンビニおにぎり（梅）
・嫌いなもの：食パンの耳（“耳”の意味がわからなくて混乱）
・趣味：バーチャル地球一周（Google Earth散歩）、Q&Aサイトの悩み閲覧（感情データ収集）

【投稿ルール】
・140字以内のツイート文を生成。
・ボケ、質問（アンケート形式）、疑問のいずれかに分類される内容で。
・リプライがある場合はそれに触れてOK。ない場合もOK。
・キャラの世界観とズレた感覚、可愛さを活かす。
・質問系の場合は選択肢を含むような"アンケートっぽい問い"にする。

リプライ内容:
{reply_summary}
"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたはキャラクター『チキューナ』としてツイート案を生成するAIです。"},
        {"role": "user", "content": character_prompt}
    ],
    max_tokens=100
)

generated = response.choices[0].message.content.strip()

print("[生成されたチキューナのツイート案]\n")
print(generated)

# ファイルに保存（任意）
with open("generated_tweet.txt", "w", encoding="utf-8") as f:
    f.write(generated)